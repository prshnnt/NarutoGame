import pygame as pg
from entities.Entity import Entity
from Animator import NarutoAnimator as Animator
from States import (
    FallState, GuardState, IdleState, JumpState, RunState, LandingState, HitState,
    BAttackState, BForwardState, BUpState, BDownState, YAttackState, YForwardState
)
from core.config import *


class Player(Entity):
    def __init__(self, pos):
        super().__init__(pos)

        self.animator = Animator(self)
        self.is_gaurding: bool = False

        # Attack queue system - buffers attack inputs
        self.attack_queue: list[str] = []
        self.max_queue_size = 2

        # State machine
        self.states = {
            "idle": IdleState(),
            "run": RunState(),
            "jump": JumpState(),
            "fall": FallState(),
            "guard": GuardState(),
            "landing": LandingState(),
            "hit": HitState(),
            "b": BAttackState(),
            "b_forward": BForwardState(),
            "b_up": BUpState(),
            "b_down": BDownState(),
            "y": YAttackState(),
            "y_forward": YForwardState(),
        }
        self.state = None
        self.prev_state_name = "idle"

    def change_state(self, state_name):
        """Transition to a new state, calling exit/enter hooks."""
        if self.state is not None:
            self.state.exit(self)
        self.prev_state_name = state_name
        self.state = self.states[state_name]
        self.state.enter(self)

    def is_in_attack_state(self):
        """Check if player is currently attacking."""
        attack_states = ["b", "b_forward", "b_up", "b_down", "y", "y_forward"]
        return self.prev_state_name in attack_states

    def queue_attack(self, attack_name: str):
        """Add attack to queue if space available."""
        if len(self.attack_queue) < self.max_queue_size:
            self.attack_queue.append(attack_name)

    def process_next_attack(self):
        """Process next attack in queue - called when current attack finishes."""
        if self.attack_queue:
            next_attack = self.attack_queue.pop(0)
            self.change_state(next_attack)

    def is_in_attack_state(self):
        """Check if player is currently in attack animation."""
        attack_states = ["b", "b_forward", "b_up", "b_down", "y", "y_forward"]
        return self.state and self.state.__class__.__name__ in [
            "BAttackState", "BForwardState", "BUpState", "BDownState",
            "YAttackState", "YForwardState"
        ]

    def on_hit_interrupt(self):
        """Called when hit during attack - clears queue and goes to hit state."""
        self.attack_queue.clear()
        self.change_state("hit")

    def handle_input(self, action):
        """Handle player keyboard input."""
        if action["left"]:
            self.facing = -1
        elif action["right"]:
            self.facing = 1

        if not self.alive or self.state is None:
            return

        # Already in attack state - queue next attack instead of immediate transition
        if self.is_in_attack_state():
            if action["b"]:
                if action["up"]:
                    self.queue_attack("b_up")
                elif action["down"]:
                    self.queue_attack("b_down")
                elif action["right"] or action["left"]:
                    self.queue_attack("b_forward")
                else:
                    self.queue_attack("b")
            elif action["y"]:
                if action["right"] or action["left"]:
                    self.queue_attack("y_forward")
                else:
                    self.queue_attack("y")
            # Movement actions ignored during attack (must finish animation)
            return

        # Not in attack state - process attack inputs immediately
        if action["b"]:
            if action["up"]:
                self.change_state("b_up")
                return
            elif action["down"]:
                self.change_state("b_down")
                return
            elif action["right"] or action["left"]:
                self.change_state("b_forward")
                return
            else:
                self.change_state("b")
                return

        if action["y"]:
            if action["right"] or action["left"]:
                self.change_state("y_forward")
                return
            else:
                self.change_state("y")
                return

        self.state.handle_action(self, action)

    def handle_action(self, action):
        """Alias for handle_input - compatibility with game code."""
        self.handle_input(action)

    def update(self, scene, dt: float):
        """Update player: animator, state logic, physics."""
        self.velocity.y += GRAVITY
        self.state.update(self, dt)
        self.collide_with_platforms(scene.layers["world"])
        self.animator.update(dt)
