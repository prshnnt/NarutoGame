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
        self.just_landed = False
        self.frames:dict = {}
        self.frame_index = 0
        self.prev_time = pg.time.get_ticks()

    def load_frames(self,frames:dict):
        self.frames = frames

    def play(self,group:str):
        if self.group == group:
            return
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
        if current_time - self.prev_time < 150:
            return False
        else:
            self.prev_time = current_time
            return True
        
    def update(self,dt):
        if self.group is None:
            return

        if self.should_update_frame():
            self.update_frame()
        if self.group == "jump":
            if self.player.velocity.y<0:
                self.frame_index = 1
        if self.group == "fall":
            if self.player.velocity.y>0:
                self.frame_index = 0
            if self.player.velocity.y==0:
                self.just_landed = True

        self.image = self.frames[self.group][self.frame_index]
        if self.group == "stance":
            if self.just_landed:
                self.image = self.frames["fall"][1]
                self.just_landed = False
        if self.group == "guard" and self.frame_index==(len(self.frames["guard"])-1):
            self.frame_index = 2
            self.image = self.frames["guard"][self.frame_index]
            
        if self.rect is None:
            self.rect = self.image.get_rect()
        self.rect.size = self.image.get_size()
        self.rect.bottomleft = self.player.rect.bottomleft

    def draw(self, scene):
        if self.image is None:
            return

        image_to_draw = self.image
        if self.player.facing == -1:
            image_to_draw = pg.transform.flip(self.image, True, False)
        scene.screen.blit(image_to_draw, scene.camera.apply(self.rect))