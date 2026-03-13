from core.GameObject import GameObject
import pygame as pg
from core.config import *

class Ground(pg.sprite.Sprite,GameObject):
    def __init__(self,image=None):
        super().__init__()
        if image is None:
            self.image = pg.Surface((SCREEN_WIDTH,GROUND_HEIGHT))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(bottomleft=(0,SCREEN_HEIGHT))
        else:
            self.image = image
            self.rect = self.image.get_rect(bottomleft=(0,SCREEN_HEIGHT))

    def update(self,dt):
        pass

    def draw(self,screen):
        screen.blit(self.image,self.rect)