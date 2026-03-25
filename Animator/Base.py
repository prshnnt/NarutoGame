import pygame as pg
# from Scenes.Base import BaseScene
from core.config import *
from core.GameObject import GameObject
from pydantic import BaseModel
# from entities.Player import Player

class FrameState(pg.sprite.Sprite):
    def __init__(self,image:pg.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.next_state = None
        self.prev_state = None
    def enter(self):
        pass
    def exit(self):
        pass
    def next(self,state):
        self.exit()
        state.enter()
        return state



class Animator:
    def __init__(self,player:GameObject):
        self.player = player

        self.image:pg.Surface = None
        self.rect:pg.Rect = self.player.rect
        self.group = None
        self.prev_group = None
        self.frames:dict = {}
        self.frame_index = 0
        self.prev_time = pg.time.get_ticks()

    def load_frames(self,frames:dict):
        self.frames = frames

    def play(self,group:str):
        if self.group == group:
            return
        self.prev_group = self.group
        self.group = group
        self.frame_index = 0

    def get_current_frame_size(self):
        return self.image.get_size()

    def update_frame(self):
        self.frame_index += 1
        if self.frame_index >= len(self.frames[self.group]):
            self.frame_index = 0

    def should_update_frame(self):
        current_time = pg.time.get_ticks()
        if current_time - self.prev_time < 500:
            return False
        else:
            self.prev_time = current_time
            return True
    def rect_resize(self):
        if self.rect is None:
            self.rect = self.image.get_rect()
        self.rect.size = self.image.get_size()
        self.rect.bottomleft = self.player.rect.bottomleft
    def update(self,dt):
        if self.group is None:
            return
        if self.should_update_frame():
            self.update_frame()
        self.image = self.frames[self.group][self.frame_index]
        self.rect_resize()

    def draw(self, scene):
        if self.image is None:
            return

        image_to_draw = self.image
        if self.player.facing == -1:
            image_to_draw = pg.transform.flip(self.image, True, False)
        scene.screen.blit(image_to_draw, scene.camera.apply(self.rect))