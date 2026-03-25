import json,pygame
from Components import ParallaxBackground , Ground
from entities.Player import Player
from core.config import *
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
        return AssetLoader.load_data(path)
    @staticmethod
    def load_data(path:str)->dict:
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
        ground = data["world_layer"]["terrain_sprites"]["1"]
        ground = AssetLoader.load_sheet(ground)
        for j ,line in enumerate(data["map"]):
            for i , tile in enumerate(line):
                 if tile == "1":
                    layers["world"].append(Ground(TILE_SIZE[0],TILE_SIZE[1],((i-1)*TILE_SIZE[0],(j-1)*TILE_SIZE[1]),ground))
        return layers
    @staticmethod
    def load_world_width(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["world_width"]
    @staticmethod
    def load_player(name="naruto"):
        path = "assets/player/naruto.json"
        data = AssetLoader.load_data(path)
        sprite_sheet = AssetLoader.load_sheet(data["sprite_sheet"])
        bounding_box = AssetLoader.load_bounding_box(data["bounding_box"])
        frames = {}
        for group in data["animations"]:
            frames[group] = AssetLoader.get_frame_list(sprite_sheet,bounding_box[group],{"x":2.2,"y":2.2}) # change this and store scale value in naruto.json in player as it may depend on sprite so it has to be hardcoded
            
        player = Player(data["position"])
        player.animator.load_frames(frames)
        player.rect = player.animator.frames["stance"][0].get_rect()
        player.change_state("idle")
        return player