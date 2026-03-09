from enum import Enum
import pygame as pg
from core.GameObject import GameObject


class BaseScene:
    def __init__(self,game,screen:pg.Surface,objects=[]):
        self.game = game
        self.screen:pg.Surface = screen
        self.objects:list[GameObject] = objects
    def reset(self):
        pass
    def add_object(self,obj):
        self.objects.append(obj)
    def remove_object(self,obj):
        self.objects.remove(obj)
    def on_key_down(self,key):
        for obj in self.objects:
            obj.on_key_down(key)
    def on_key_pressed(self,event):
        for obj in self.objects:
            obj.on_key_pressed(event)
    def update(self):
        for obj in self.objects:
            obj.update(self.game.dt)
    def draw(self):
        for obj in self.objects:
            obj.draw(self.screen)

class MenuScene(BaseScene):
    def __init__(self,game , screen: pg.Surface):
        super().__init__(game,screen,[])

    def update(self, dt, events, mouse_pos):
        super().update(dt, events, mouse_pos)

    def draw(self):
        super().draw()
