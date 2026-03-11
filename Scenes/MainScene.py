from httpx import options

from Scenes.Base import BaseScene
import pygame as pg
from Components.Buttons import Button
from core.config import *



class MenuScene(BaseScene):
    def __init__(self,game , screen: pg.Surface):
        super().__init__(game,screen)
        self.init()
    def init(self):
        start_button = Button(width_percent(50)-50, height_percent(10), 100, 50, "START", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(GameScenes.GAME))
        options_button = Button(width_percent(50)-50, height_percent(10), 100, 50, "OPTIONS", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(GameScenes.OPTIONS))
        quit_button = Button(width_percent(50)-50, height_percent(10), 100, 50, "QUIT", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(GameScenes.QUIT))
        self.add_object(start_button,"ui")