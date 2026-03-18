import pygame as pg
import json
from States.Base import BaseState
from core.config import *
from core.GameObject import GameObject
from Animator.Base import Animator
# from States.IdleState import IdleState


GRAVITY = 800       # pixels per second squared
MAX_FALL_SPEED = 600

class Player(GameObject):
    def __init__(self, hitbox:pg.Rect):
        self.rect = hitbox
        self.position = pg.Vector2(hitbox.x,hitbox.y)
        self.velocity = pg.Vector2(0,0)
        # only animator will draw the player and sprites timing and which sprite to play and size will be hard coded
        self.animator = Animator(self)
        
        self.in_air = True

        # --- Stats ---
        self.health: int = 100
        self.alive: bool = True
        self.facing: int = 1           # 1 = right, -1 = left
        self.dt = 0

        # --- State machine: start in idle ---
        self.state = None
        # self.change_state(IdleState())
    # ------------------------------------------------------------------ #
    #  State machine                                                       #
    # ------------------------------------------------------------------ #

    def change_state(self, new_state):
        """Transition to a new state, calling exit/enter hooks."""
        if self.state is not None:
            self.state.exit(self)
        self.state:BaseState= new_state
        self.state.enter(self)

    def draw(self,scene):
        """Delegate drawing to current state (which calls animator)."""
        self.animator.draw(scene)

    def handle_input(self, keys):
        if self.alive:
            self.state.handle_input(self, keys)

    def update(self,scene , dt: float):
        """Update state logic, move the rect, resolve collisions."""
        # self.state.update(self)
        self.animator.update(dt)

    def _resolve_collisions(self, platforms: list[pg.Rect]):
        """Simple AABB collision resolution against a list of platform rects."""
        for platform in platforms:
            if self.rect.colliderect(platform):
                # Falling down — land on top
                if self.vel_y > 0 and self.rect.bottom - int(self.vel_y * 0.02) <= platform.top + 10:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                # Jumping up — hit ceiling
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
                # Moving right — hit wall
                elif self.vel_x > 0:
                    self.rect.right = platform.left
                # Moving left — hit wall
                elif self.vel_x < 0:
                    self.rect.left = platform.right

    # ------------------------------------------------------------------ #
    #  Combat helpers (called externally by game logic)                   #
    # ------------------------------------------------------------------ #

    def take_damage(self, amount: int):
        """Apply damage and switch to HitState or DeadState."""
        from States.HitState import HitState
        from States.DeadState import DeadState

        if not self.alive or self.is_guarding:
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.change_state(DeadState())
        else:
            self.change_state(HitState())