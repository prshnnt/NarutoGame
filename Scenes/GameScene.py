from Scenes.Base import BaseScene
from Components.Buttons import Button
from core.SpriteSheetLoader import load_sheet
from core.AssetLoader import AssetLoader
from core.config import *

class GameScene(BaseScene):
    def on_enter(self):
        self.layers = AssetLoader.load_level("assets/levels/level1.json")
        self.world_width = AssetLoader.load_world_width("assets/levels/level1.json")
        sheets = []
        for i in range(1,6):
            sheets.append(load_sheet(f'assets/images/background/plx-{i}.png'))
        start_button = Button(width_percent(1), height_percent(1), 50, 50, "||", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.MENU))
        self.add_object(start_button,"ui")
    def scroll_left(self):
        self.scroll -= RUN_SPEED
    def scroll_right(self):
        self.scroll += RUN_SPEED
    def make_background_infinite(self):
        ls = []
        for background in self.layers["background"]:
            ls.append(background.)