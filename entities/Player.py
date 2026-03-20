import pygame as pg
import json
from Components import Ground
from States.Base import BaseState
from core.config import *
from core.GameObject import GameObject
from Animator.Base import Animator
from States import FallState, IdleState, JumpState, RunState


class Player(GameObject):
    def __init__(self, pos):
        self.rect = None
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0,0)
        # only animator will draw the player and sprites timing and which sprite to play and size will be hard coded
        self.animator = Animator(self)
        
        self.in_air = True

        self.health: int = 100
        self.invincible: bool = False
        self.alive: bool = True
        self.facing: int = 1           # 1 = right, -1 = left
        self.dt = 0

        #State machine: start in idle
        self.states = {
            "idle": IdleState(),
            "run": RunState(),
            "jump": JumpState(),
            "fall": FallState(),
        }
        self.state = None # didnt set state because i am setting state in asset loader when asset are loaded

    def change_state(self, state):
        """Transition to a new state, calling exit/enter hooks."""
        print(f"Changing state to {state}")
        if self.state is not None:
            self.state.exit(self)
        self.state = self.states[state]
        self.state.enter(self)


    def handle_action(self, action):
        if action["left"]:
            self.facing = -1
        if action["right"]:
            self.facing = 1
        if self.alive and self.state is not None:
            self.state.handle_action(self,action)
    def move_x(self):
        self.position.x += self.velocity.x
        self.rect.x = self.position.x
    def move_y(self):
        self.position.y += self.velocity.y
        self.rect.y = self.position.y

    def collide_wall(self,platforms:list[Ground]):
        # --- X AXIS MOVEMENT ---
        self.move_x()
        # X Collision Check
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right
                
                # CRITICAL FIX: Sync self.x with the new rect position
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
                
                # CRITICAL FIX: Sync self.y with the new rect position
                self.position.y = self.rect.y

    def update(self,scene , dt: float):
        """Update state logic, move the rect, resolve collisions."""
        self.velocity.y += GRAVITY 

        self.state.update(self,dt)

        self.collide_wall(scene.layers["world"])

        self.animator.update(dt)
        
    def draw(self,scene):
        """Delegate drawing to animator"""
        if self.invincible:
            if (pg.time.get_ticks() // 100) % 2 == 0:
                return
        # pg.draw.rect(scene.screen,RED,scene.camera.apply(self.rect))
        self.animator.draw(scene)
