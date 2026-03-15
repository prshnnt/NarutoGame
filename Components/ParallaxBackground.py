import pygame as pg

from core.GameObject import GameObject

class ParallaxBackground(GameObject):
    def __init__(self,image:pg.Surface,speed):
        self.image = image
        self.speed = speed
        self.width = image.get_width()
    def update(self, scene):
        return super().update(scene)
    def draw(self,scene):
        offsetx = scene.camera.rect.x * self.speed
        x = -offsetx % self.width
        scene.screen.blit(self.image, (x,0))
        scene.screen.blit(self.image, (x-self.width,0))
        scene.screen.blit(self.image, (x+self.width,0))