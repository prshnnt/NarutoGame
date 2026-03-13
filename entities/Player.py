from enum import Enum

import pygame
from core.SpriteSheetLoader import get_frame_list, load_sheet , load_bounding_box
from core.config import COLORKEY
from core.GameObject import GameObject

import pygame

from States.IdleState import IdleState


class Player:

    def __init__(self, pos):

        self.rect = pygame.Rect(pos[0], pos[1], 40, 60)

        self.vel = pygame.Vector2(0, 0)

        self.speed = 250
        self.jump_force = 450
        self.gravity = 1000

        self.on_ground = False

        self.state = IdleState()
        self.state.enter(self)

        self.controls = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_SPACE
        }

        self.keys = None

    def change_state(self, new_state):

        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def handle_input(self, keys):

        self.keys = keys
        self.state.handle_input(self, keys)

    def update(self, dt):

        self.state.update(self, dt)

        # apply gravity
        self.vel.y += self.gravity * dt

        # move
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt

        # ground collision (simple)
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

# class PlayerState(Enum):
#     STANCE = 0
#     RUN = 1
#     JUMP = 2
#     HIT = 3
#     DOWN = 4
#     GUARD = 5
#     B = 6
#     B_FORWARD = 7
#     B_UP = 8
#     B_DOWN = 9
#     Y = 10
#     Y_FORWARD = 11
#     Y_UP = 12
#     DASH_ATTACK =13
#     JUMP_B = 14
#     JUMP_Y = 15