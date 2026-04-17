import pygame as pg
from abc import ABC, abstractmethod
from core.config import *


class Entity(ABC):
    """
    Base class for all game entities (Player, Enemy).
    Shared functionality: position, velocity, health, states, collision.
    """
    def __init__(self, pos):
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0, 0)
        self.rect = pg.Rect(pos[0], pos[1], 50, 50)  # Default size until animator sets it

        self.in_air = True
        self.health: int = 100
        self.invincible: bool = False
        self.alive: bool = True
        self.facing: int = 1           # 1 = right, -1 = left
        self.dt = 0

        # Attack hitbox
        self.attack_hitbox: pg.Rect = None
        self.attack_damage: int = 10
        self.hitbox_duration: int = 200  # ms
        self.hitbox_timer: float = 0

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
        self.update_hitbox(dt)

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

    def create_hitbox(self, width: int, height: int, offset_x: int = 0):
        """Create attack hitbox in front of entity based on facing direction."""
        if self.facing == 1:
            hitbox_x = self.rect.right + offset_x
        else:
            hitbox_x = self.rect.left - width - offset_x

        hitbox_y = self.rect.top + (self.rect.height - height) // 2
        self.attack_hitbox = pg.Rect(hitbox_x, hitbox_y, width, height)
        self.hitbox_timer = self.hitbox_duration / 1000

    def update_hitbox(self, dt: float):
        """Update hitbox timer and clear when expired."""
        if self.attack_hitbox is not None:
            self.hitbox_timer -= dt
            if self.hitbox_timer <= 0:
                self.attack_hitbox = None

    def check_hit(self, target: 'Entity') -> bool:
        """Check if attack hitbox collides with target."""
        if self.attack_hitbox is not None and target.rect is not None:
            return self.attack_hitbox.colliderect(target.rect)
        return False
