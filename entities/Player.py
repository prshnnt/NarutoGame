import pygame as pg
from entities.Entity import Entity
from Animator import NarutoAnimator as Animator
from States import (
    FallState, GuardState, IdleState, JumpState, RunState, LandingState,
    BAttackState, BForwardState, BUpState, BDownState, YAttackState, YForwardState
)
from core.config import *


class Player(Entity):
    def __init__(self, pos):
        super().__init__(pos)

        self.animator = Animator(self)
        self.is_gaurding: bool = False
        self.is_attacking: bool = False

        # State machine
        self.states = {
            "idle": IdleState(),
            "run": RunState(),
            "jump": JumpState(),
            "fall": FallState(),
            "guard": GuardState(),
            "landing": LandingState(),
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

    def handle_input(self, action):
        """Handle player keyboard input."""
        if action["left"]:
            self.facing = -1
        elif action["right"]:
            self.facing = 1

        if not self.alive or self.state is None:
            return

        # Attack inputs (priority over movement)
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
