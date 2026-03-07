import pygame
import json

def load_sheet(path:str)->pygame.Surface:
    sheet = pygame.image.load(path).convert_alpha()
    return sheet

def load_bounding_box(path:str)->dict:
    with open(path, "r") as f:
        data = json.load(f)
    return data

def get_frame(sheet,frame,scale) -> pygame.Surface:
    rect = pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"])
    img = pygame.Surface((frame["w"], frame["h"]), pygame.SRCALPHA)
    img.set_colorkey((0,64,128))
    img.blit(sheet, (0, 0), rect)
    img = img.convert_alpha(img)
    img = pygame.transform.scale(img, (frame["w"]*scale["x"], frame["h"]*scale["y"]))
    return img