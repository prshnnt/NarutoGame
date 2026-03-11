from Scenes.Base import BaseScene
import pygame as pg
from Components.Buttons import Button
from core.config import *

class GameScene(BaseScene):
    def __init__(self,game , screen: pg.Surface):
        super().__init__(game,screen)
    def on_enter(self):
        start_button = Button(width_percent(1), height_percent(1), 50, 50, "||", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.MENU))
        self.add_object(start_button,"ui")