import pygame as pg
from abc import ABC, abstractmethod
from core.config import *


class Entity(ABC):
    """
    Base class for all game entities (Player, Enemy).
    Shared functionality: position, velocity, health, states, collision.
    """
    def __init__(self, pos):
        self.rect = None
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)

        self.in_air = True
        self.health: int = 100
        self.invincible: bool = False
        self.alive: bool = True
        self.facing: int = 1           # 1 = right, -1 = left
        self.dt = 0

        # State machine
        self.states = {}
        self.state = None

    @abstractmethod
    def change_state(self, state_name):
        """Transition to a new state."""
        pass

    @abstractmethod
    def handle_input(self, action):
        """Handle input/action - player uses keyboard, enemy uses AI."""
        pass

    def move_x(self):
        self.position.x += self.velocity.x
        self.rect.x = self.position.x

    def move_y(self):
        self.position.y += self.velocity.y
        self.rect.y = self.position.y

    def collide_with_platforms(self, platforms: list):
        # --- X AXIS MOVEMENT ---
        self.move_x()
        # X Collision Check
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right

                self.position.x = self.rect.x

        # --- Y AXIS MOVEMENT ---
        self.in_air = True
        self.move_y()
        # Y Collision Check
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.in_air = False
                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

                self.position.y = self.rect.y

    def update(self, scene, dt: float):
        """Update state logic, move the rect, resolve collisions."""
        self.velocity.y += GRAVITY
        self.state.update(self, dt)
        self.collide_with_platforms(scene.layers["world"])

    def draw(self, scene):
        """Delegate drawing to animator"""
        if self.invincible:
            if (pg.time.get_ticks() // 100) % 2 == 0:
                return
        self.animator.draw(scene)

    def take_damage(self, amount: int):
        """Apply damage to entity."""
        if not self.invincible and self.alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
