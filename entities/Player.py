from enum import Enum

from core.Base import GameObject
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

    
# class Player(GameObject):
#     """
#     Represents the player character.
#     """

#     def __init__(self,scene):
#         self.scene = scene
#         # self.active_state = PlayerState.STANCE
#         self.current_state = PlayerState.STANCE
#         self.direction = 1  # 1 for right, -1 for left
#         self.frame_index = 0
#         self.animation_states_functions = {
#             PlayerState.STANCE: self.iter_frame,
#             PlayerState.RUN: self.iter_frame,
#             # PlayerState.JUMP: [],
#             # PlayerState.HIT: [],
#             # PlayerState.DOWN: [],
#             # PlayerState.GUARD: [],
#             # PlayerState.B: [],
#             # PlayerState.B_FORWARD: [],
#             # PlayerState.B_UP: [],
#             # PlayerState.B_DOWN: [],
#             # PlayerState.Y: [],
#             # PlayerState.Y_FORWARD: [],
#             # PlayerState.Y_UP: [],
#             # PlayerState.DASH_ATTACK: [],
#             # PlayerState.JUMP_B: [],
#             # PlayerState.JUMP_Y: []

#         }

#         self.animation_sprites = {
#             PlayerState.STANCE: [],
#             PlayerState.RUN: [],
#             # PlayerState.JUMP: [],
#             # PlayerState.HIT: [],
#             # PlayerState.DOWN: [],
#             # PlayerState.GUARD: [],
#             # PlayerState.B: [],
#             # PlayerState.B_FORWARD: [],
#             # PlayerState.B_UP: [],
#             # PlayerState.B_DOWN: [],
#             # PlayerState.Y: [],
#             # PlayerState.Y_FORWARD: [],
#             # PlayerState.Y_UP: [],
#             # PlayerState.DASH_ATTACK: [],
#             # PlayerState.JUMP_B: [],
#             # PlayerState.JUMP_Y: []
#         }

#         self.load_sprites()
#     def get_state(self):
#         return self.current_state
#     def set_state(self,state):
#         if self.in_air and not self.current_state == PlayerState.JUMP
#         if self.current_state != state:
#             self.current_state = state
#             self.frame_index = 0


#     def on_key_down(self,key):
#         if key == pygame.K_LEFT:
#             self.current_state = PlayerState.RUN
#         elif key == pygame.K_RIGHT:
#             self.current_state = PlayerState.RUN
#         elif key == pygame.K_UP:
#             self.current_state = PlayerState.JUMP
#     def on_key_pressed(self,event):
#         pass
#     def load_sprites(self):
#         sheet = load_sheet("assets/images/Naruto.png").convert_alpha()
#         sheet.set_colorkey(COLORKEY)
#         bounding_box = load_bounding_box("assets/bounding_box/Naruto.json")
#         self.animation_sprites[PlayerState.STANCE] = get_frame_list(sheet,bounding_box["stance"],(3,3))
#         self.animation_sprites[PlayerState.RUN] = get_frame_list(sheet,bounding_box["run"],(3,3))
#         self.animation_sprites[PlayerState.JUMP] = get_frame_list(sheet,bounding_box["jump"],(3,3))

#     def iter_animate(self):
#         self.frame_index += 1
#         if self.frame_index >= len(self.animation_sprites[PlayerState.STANCE]):
#             self.frame_index = 0
#         return self.animation_sprites[self.active_state][self.frame_index]
#     def update(self):
#         self.animation_states_functions[self.active_state]()
#     def draw(self, surface):
#         surface.blit(self.animation_sprites[self.active_state][self.frame_index], (0, 0))