from Scenes.Base import BaseScene
import pygame as pg
from Components.Buttons import Button
from core.config import *

class MenuScene(BaseScene):
    def __init__(self,game , screen: pg.Surface):
        super().__init__(game,screen)
    def on_enter(self):
        start_button = Button(width_percent(50)-50, height_percent(12), 100, 50, "START", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.GAME))
        options_button = Button(width_percent(50)-50, height_percent(12)*3, 100, 50, "OPTIONS", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.OPTIONS))
        quit_button = Button(width_percent(50)-50, height_percent(12)*5, 100, 50, "QUIT", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.QUIT))
        self.add_object(start_button,"ui")
        self.add_object(options_button,"ui")
        self.add_object(quit_button,"ui")     