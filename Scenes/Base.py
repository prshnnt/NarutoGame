from enum import Enum
import pygame as pg
from core.GameObject import GameObject


class BaseScene:
    def __init__(self,game,screen:pg.Surface):
        self.game = game
        self.screen:pg.Surface = screen
        # Scene
        # ├ background layer
        # ├ world layer
        # │   ├ terrain
        # │   ├ player
        # │   ├ enemies
        # │   └ bullets
        # ├ particle layer
        # └ ui layer
        # This ensures:
        # background → world → effects → UI
        
        self.layers:dict[str,list[GameObject]] = {
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
    def handle_action(self,action):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                obj.handle_action(action)


    def add_object(self, obj, layer="world"):
        self.layers[layer].append(obj)
    
    def remove_object(self,obj,layer="world"):
        if obj in self.layers[layer]:
            self.layers[layer].remove(obj)

    def update(self,dt):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                obj.update(self)

    def draw(self):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                obj.draw(self)