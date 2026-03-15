import json,pygame

from Components.ParallaxBackground import ParallaxBackground
from Components.Background import Background
from Components.Ground import Ground
# from core.SpriteSheetLoader import load_sheet
# from entities import Player
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
    
class AssetLoader:
    @staticmethod
    def load_sheet(path:str)->pygame.Surface:
        sheet = pygame.image.load(path).convert_alpha()
        return sheet
    @staticmethod
    def load_bounding_box(path:str)->dict:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    @staticmethod
    def get_frame(sheet,frame,scale) -> pygame.Surface:
        rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
        img = pygame.Surface((frame["w"], frame["h"]), pygame.SRCALPHA)
        img.set_colorkey((0,64,128))
        img.blit(sheet, (0, 0), rect)
        img = img.convert_alpha(img)
        img = pygame.transform.scale(img, (frame["w"]*scale["x"], frame["h"]*scale["y"]))
        return img
    @staticmethod
    def get_frame_list(sheet,frames,scale) -> list:
        img_list = []
        for frame in frames:
            img_list.append(AssetLoader.get_frame(sheet,frame,scale))
        return img_list
    @staticmethod
    def load_level(path):
        layers = {
            "background":[],
            "world":[],
            "effects":[],
            "ui":[]
        }
        with open(path, "r") as f:
            data = json.load(f)
        for img,speed in zip(data["background"]["sprites"],data["background"]["speeds"]):
            layers["background"].append(
                ParallaxBackground(AssetLoader.load_sheet(img),speed)
                )
        layers["world"].append(Ground())
        return layers
    @staticmethod
    def load_world_width(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["world_width"]
    @staticmethod
    def load_player():
        path = "assets/images/Naruto.png"
        bb_path = "assets/bounding_box/naruto.json"
        sheet = AssetLoader.load_sheet(path)
        bounding_box = AssetLoader.load_bounding_box(bb_path)
        # player = Player()