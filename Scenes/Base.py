from enum import Enum
import pygame as pg
from core.GameObject import GameObject


class BaseScene:
    def __init__(self,game,screen:pg.Surface):
        self.game = game
        self.screen:pg.Surface = screen
        self.layers = {
            "background":[],
            "world":[],
            "effects":[],
            "ui":[]
        }
    
    def on_enter(self):
        pass

    def on_exit(self):
        for layer in  ["background", "world", "effects", "ui"]:
            self.layers[layer].clear()
    def handle_event(self,event):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                obj.handle_event(event)


    def add_object(self, obj, layer="world"):
        self.layers[layer].append(obj)
    
    def remove_object(self,obj,layer="world"):
        if obj in self.layers[layer]:
            self.layers[layer].remove(obj)

    def update(self,dt):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                obj.update(dt)

    def draw(self):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                obj.draw(self.screen)


