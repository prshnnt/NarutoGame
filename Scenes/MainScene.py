from Scenes.Base import BaseScene
import pygame as pg
from Components.Buttons import Button
from core.config import *



class MenuScene(BaseScene):
    def __init__(self,game , screen: pg.Surface):
        super().__init__(game,screen)
    def init(self):
        start_button = Button(40,20,
                              50,20,
                              "START",
                              None,
                              YELLOW,
                              PURPLE,
                              lambda : self.game.change_scene(GameScenes.GAME))
        self.add_object(start_button,"ui")