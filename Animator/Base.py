import pygame as pg
# from Scenes.Base import BaseScene
from core.config import *
from core.GameObject import GameObject
# from entities.Player import Player


class Animator:
    def __init__(self,player:GameObject):
        self.player = player

        self.image:pg.Surface = None
        self.rect:pg.Rect = self.player.rect
        self.group = None
        self.frames:dict = {}
        self.frame_index = 0
        self.prev_time = pg.time.get_ticks()

    def load_frames(self,frames:dict):
        self.frames = frames

    def play(self,group:str):
        self.group = group
        self.image = self.frames[group][0]

    def get_current_frame_size(self):
        return self.image.get_size()
    def update_frame(self):
        self.frame_index += 1
        if self.frame_index >= len(self.frames[self.group]):
            self.frame_index = 0
    def delta_time(self,dt):
        current_time = pg.time.get_ticks()
        if current_time - self.prev_time < 200:
            return False
        else:
            self.prev_time = current_time
            return True

    def update(self,dt):
        if self.group is None:
            return
        if not self.delta_time(dt):
            return
        self.update_frame()
        self.image = self.frames[self.group][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.player.rect.bottomleft

    def draw(self,scene):
        if self.player.facing == -1:
            self.image = pg.transform.flip(self.image, True, False)
        scene.screen.blit(self.image, self.rect)