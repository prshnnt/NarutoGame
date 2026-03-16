import pygame as pg
import json
from core.config import *

from core.Animator import Animator
from core.AssetLoader import AssetLoader
from States.IdleState import IdleState


GRAVITY = 800       # pixels per second squared
MAX_FALL_SPEED = 600

class Player:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        self.vel_x = 0
        self.vel_y = 0
        # only animator will draw the player and sprites timing and which sprite to play and size will be hard coded
        self.animator = Animator(self.rect.center)
        self.animator.play("stance")
        
        self.on_ground: bool = False
        self.speed: int = PLAYER_SPEED         # horizontal speed (px/s)
        self.jump_force: int = JUMP_FORCE     # initial upward velocity on jump

        # --- Stats ---
        self.health: int = 100
        self.alive: bool = True
        self.is_guarding: bool = False
        self.facing: int = 1           # 1 = right, -1 = left

        # --- Controls (defaults to arrow keys + z/x) ---
        self.controls = {
            "left":   pg.K_LEFT,
            "right":  pg.K_RIGHT,
            "jump":   pg.K_z,
            "guard":  pg.K_x,
            "attack": pg.K_a,
        }

        # --- State machine: start in idle ---
        self.state = None
        self.change_state(IdleState())
    # ------------------------------------------------------------------ #
    #  State machine                                                       #
    # ------------------------------------------------------------------ #

    def change_state(self, new_state):
        """Transition to a new state, calling exit/enter hooks."""
        if self.state is not None:
            self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def draw(self, screen: pg.Surface, scroll: int):
        """Delegate drawing to current state (which calls animator)."""
        self.state.draw(self, screen, scroll)



    # ------------------------------------------------------------------ #
    #  Core loop                                                           #
    # ------------------------------------------------------------------ #

    def handle_input(self, keys):
        if self.alive:
            self.state.handle_input(self, keys)

    def update(self, dt: float, platforms: list[pg.Rect]):
        """Update state logic, move the rect, resolve collisions."""
        if not self.alive:
            self.state.update(self, dt)
            return

        self.state.update(self, dt)

        # Apply horizontal movement
        self.rect.x += int(self.vel_x * dt)

        # Apply vertical movement
        self.rect.y += int(self.vel_y * dt)

        # Collision detection
        self.on_ground = False
        self._resolve_collisions(platforms)

        # Sync animator facing
        self.animator.facing = self.facing
        self.animator.update(dt)

        # Keep rect size in sync with current animation frame
        w, h = self.animator.get_current_frame_size()
        self.rect.width = w
        self.rect.height = h

    # ------------------------------------------------------------------ #
    #  Physics helpers                                                     #
    # ------------------------------------------------------------------ #

    def apply_gravity(self, dt: float):
        self.vel_y += GRAVITY * dt
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

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