import pygame as pg
import random
from entities.Entity import Entity
from Animator import NarutoAnimator as Animator
from States import FallState, GuardState, IdleState, JumpState, RunState, LandingState


class Enemy(Entity):
    """
    Enemy class controlled by AI.
    Inherits shared functionality from Entity.
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

        # State machine - same states as player
        self.states = {
            "idle": IdleState(),
            "run": RunState(),
            "jump": JumpState(),
            "fall": FallState(),
            "guard": GuardState(),
            "landing": LandingState()
        }
        self.state = None

    def change_state(self, state_name):
        """Transition to a new state."""
        print(f"Enemy changing state to {state_name}")
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
            "attack": False
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

        # Attack range
        if distance <= self.attack_range:
            action["attack"] = True
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

    def handle_input(self, action):
        """Handle AI-generated input."""
        if action["left"]:
            self.facing = -1
        elif action["right"]:
            self.facing = 1

        if self.alive and self.state is not None:
            self.state.handle_action(self, action)

    def update_ai(self, dt: float):
        """Update AI decision making."""
        self.ai_timer += dt

        if self.ai_timer >= self.ai_interval:
            self.ai_timer = 0
            self.ai_interval = random.uniform(0.5, 2.0)

            # Generate and apply AI input
            ai_action = self._generate_ai_input()

            if ai_action["attack"]:
                # Attack logic handled in state
                pass

            self.handle_input(ai_action)

    def update(self, scene, dt: float):
        """Update enemy: AI, animator, state logic, physics."""
        self.update_ai(dt)
        self.velocity.y += GRAVITY
        self.state.update(self, dt)
        self.collide_with_platforms(scene.layers["world"])
        self.animator.update(dt)
