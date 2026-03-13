from Scenes.Base import BaseScene
from Components.Buttons import Button
from core.Camera import Camera
from core.SpriteSheetLoader import load_sheet
from core.AssetLoader import AssetLoader
from core.config import *
from entities.Player import Player
import pygame as pg

class GameScene(BaseScene):
    def on_enter(self):
        pause_button = Button(width_percent(1), height_percent(1), 50, 50, "||", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.MENU))
        self.add_object(pause_button,"ui")
        self.layers = AssetLoader.load_level("assets/levels/level1.json")
        self.world_width = AssetLoader.load_world_width("assets/levels/level1.json")

        self.camera = Camera(self.world_width,SCREEN_HEIGHT)
        self.player = Player((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

    def update(self,dt):
        self.player.handle_input(keys)
        self.camera.update(self.player.rect)

        keys = pg.key.get_pressed()
        super().update(dt)

    def scroll_left(self):
        self.scroll -= RUN_SPEED
    def scroll_right(self):
        self.scroll += RUN_SPEED