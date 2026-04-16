import pygame as pg
from entities.Entity import Entity
from Animator import NarutoAnimator as Animator
from States import FallState, GuardState, IdleState, JumpState, RunState, LandingState
from core.config import *



class Player(Entity):
    def __init__(self, pos):
        super().__init__(pos)

        self.animator = Animator(self)
        self.is_gaurding: bool = False

        # State machine
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
        """Transition to a new state, calling exit/enter hooks."""
        print(f"Changing state to {state_name}")
        if self.state is not None:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    def handle_input(self, action):
        """Handle player keyboard input."""
        if action["left"]:
            self.facing = -1
        elif action["right"]:
            self.facing = 1

        if self.alive and self.state is not None:
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
