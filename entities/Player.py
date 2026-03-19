import pygame as pg
import json
from States.Base import BaseState
from core.config import *
from core.GameObject import GameObject
from Animator.Base import Animator
from States import FallState, IdleState, JumpState, RunState


GRAVITY = 1      # pixels per second squared

class Player(GameObject):
    def __init__(self, pos):
        self.rect = None
        self.position = pg.Vector2(pos)
        self.velocity = pg.Vector2(0,0)
        # only animator will draw the player and sprites timing and which sprite to play and size will be hard coded
        self.animator = Animator(self)
        
        self.in_air = True

        self.health: int = 100
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
    def move(self):
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def update(self,scene , dt: float):
        """Update state logic, move the rect, resolve collisions."""
        self.velocity.y += GRAVITY 

        self.state.update(self,dt)

        self.move()

        # THEN check collision
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            if self.in_air:
                self.change_state("idle")
            self.in_air = False
            self.velocity.y = 0
        else:
            if not self.in_air:
                self.change_state("fall")
            self.in_air = True

        self.animator.update(dt)
        
    def draw(self,scene):
        """Delegate drawing to animator"""
        pg.draw.rect(scene.screen,RED,self.rect)
        self.animator.draw(scene)