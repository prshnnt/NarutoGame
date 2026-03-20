from core.GameObject import GameObject
import pygame as pg
from core.config import *

class Ground(pg.sprite.Sprite,GameObject):
    def __init__(self,width,height,pos=(0,SCREEN_HEIGHT-GROUND_HEIGHT),image=None):
        super().__init__()
        if image is None:
            self.image = pg.Surface((width,height))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(topleft = pos)
        else:
            self.image = image
            self.rect = self.image.get_rect(bottomleft=(0,SCREEN_HEIGHT))

    def update(self,game):
        pass

    def draw(self,scene):
        scene.screen.blit(self.image,scene.camera.apply(self.rect))