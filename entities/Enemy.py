import pygame as pg
import random
from entities.Entity import Entity
from Animator import NarutoAnimator as Animator
from States import FallState, GuardState, IdleState, JumpState, RunState, LandingState
from States.BAttackState import BAttackState
from core.config import *


class Enemy(Entity):
    """
    Enemy class controlled by AI.
    Inherits shared functionality from Entity.

    Structure:                                                                                                                                   
    entities/                                                                                                                                      ├── Entity.py    # Base class (shared: position, velocity, health, states, collision)
    ├── Player.py    # Inherits Entity (keyboard input)                                                                                            ├── Enemy.py     # Inherits Entity (AI control)                                                                                                └── __init__.py  # Package exports                                                                                                                                                                                                                                                            Entity base class:                                                                                                                             - Position, velocity, health, invincibility, facing direction                                                                                  - State machine with enter/exit hooks                                                                                                          - Collision detection (X/Y axis)                                                                                                               - take_damage() method                                                                                                                                                                                                                                                                      
    Player:
    - Human control via handle_input(action)
    - Same states: idle, run, jump, fall, guard, landing

    Enemy:
    - AI control with aggro range (300px) and attack range (50px)
    - Chases player, attacks when close, random jumps
    - set_target(player) to assign target

    Usage:
    from entities import Player, Enemy

    player = Player((100, 100))
    enemy = Enemy((400, 100))
    enemy.set_target(player)
    """
    def __init__(self, pos):
        super().__init__(pos)

        self.animator = Animator(self)

        # AI behavior
        self.ai_state = "idle"
        self.ai_timer = 0
        self.ai_interval = random.uniform(0.5, 2.0)
        self.target = None

        # Aggro settings
        self.aggro_range = 300
        self.attack_range = 50

        # Attack settings
        self.is_attacking: bool = False
        self.attack_damage: int = 10

        # State machine - same states as player
        self.states = {
            "idle": IdleState(),
            "run": RunState(),
            "jump": JumpState(),
            "fall": FallState(),
            "guard": GuardState(),
            "landing": LandingState(),
            "b": BAttackState()
        }
        self.state = None

    def change_state(self, state_name):
        """Transition to a new state."""
        if self.state is not None:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    def set_target(self, target):
        """Set the player as target for AI."""
        self.target = target

    def _generate_ai_input(self):
        """Generate AI input based on target distance and state."""
        action = {
            "left": False,
            "right": False,
            "space": False,
            "g": False,
            "b": False
        }

        if self.target is None or not self.target.alive:
            return action

        dx = self.target.position.x - self.position.x
        dy = self.target.position.y - self.position.y
        distance = abs(dx)

        # Face target
        if dx > 0:
            self.facing = 1
        else:
            self.facing = -1

        # In air - just fall
        if self.in_air:
            return action

        # Already attacking - wait
        if self.is_attacking:
            return action

        # Attack range - trigger attack
        if distance <= self.attack_range:
            action["b"] = True
            return action

        # Chase target
        if distance <= self.aggro_range:
            if dx > 0:
                action["right"] = True
            else:
                action["left"] = True

            # Jump over obstacles
            if dy < -50 and random.random() < 0.02:
                action["space"] = True

        return action

    def is_in_attack_state(self):
        """Check if enemy is currently attacking."""
        return self.state and self.state.__class__.__name__ == "BAttackState"

    def handle_input(self, action):
        """Handle AI-generated input."""
        if action["left"]:
            self.facing = -1
        elif action["right"]:
            self.facing = 1

        if not self.alive or self.state is None:
            return

        # Attack input (priority)
        if action["b"]:
            self.change_state("b")
            return

        self.state.handle_action(self, action)

    def update_ai(self, dt: float):
        """Update AI decision making."""
        self.ai_timer += dt

        if self.ai_timer >= self.ai_interval:
            self.ai_timer = 0
            self.ai_interval = random.uniform(0.5, 2.0)

            # Generate and apply AI input
            ai_action = self._generate_ai_input()
            self.handle_input(ai_action)

    def update(self, scene, dt: float):
        """Update enemy: AI, animator, state logic, physics."""
        self.update_ai(dt)
        self.velocity.y += GRAVITY
        self.state.update(self, dt)
        self.collide_with_platforms(scene.layers["world"])
        self.animator.update(dt)
