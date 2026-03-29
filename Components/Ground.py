import random

from core.GameObject import GameObject
import pygame as pg
from core.config import *

class Ground(pg.sprite.Sprite,GameObject):
    def __init__(self,width,height,pos=(0,SCREEN_HEIGHT-GROUND_HEIGHT),image=None):
        super().__init__()
        self.image = pg.Surface((width,height))
        if image is None:
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(topleft = pos)
        else:
            section_width = image.get_width() // 3
            # Define the area to cut from the source image
            source_area = pg.Rect(random.choice((0, 1, 2)) * section_width, 0, width, height)
            # Blit that specific area onto our sprite's image
            self.image.blit(image, (0, 0), source_area)
            # Now create the sprite's rect and position it
            self.rect = self.image.get_rect(topleft = pos)

    def update(self,game):
        pass
    def draw(self,scene):
        scene.screen.blit(self.image,scene.camera.apply(self.rect))