import pygame as pg
from core.GameObject import GameObject

class Background(pg.sprite.Sprite,GameObject):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self, game):
        pass

    def draw(self, game):
        game.screen.blit(self.image, self.rect)