from Scenes.Base import BaseScene
from Components import Button, Text
from core.config import *

class OptionScene(BaseScene):
    def on_enter(self):
        text = Text(width_percent(0),height_percent(10),
                    "Sound")
        sound_button = Button(width_percent(50)-25, height_percent(10), 50, 20, "OFF", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              choice=["OFF","ON"])
        sound_button.callback = lambda: sound_button.toggle_choice()
        self.add_object(text,"ui")
        self.add_object(sound_button, "ui")

        back_button = Button(width_percent(1), height_percent(1),50,20,"BACK",None,YELLOW,PURPLE,BLACK,lambda: self.game.change_scene(MainScenes.MENU))
        self.add_object(back_button,"ui")