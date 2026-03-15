import pygame
from enum import Enum


SCREEN_WIDTH:int = 960
SCREEN_HEIGHT:int = 475
GROUND_HEIGHT:int = 50
RUN_SPEED = SCROLL_SPEED = 5
PLAYER_SPEED = 10
JUMP_FORCE = 50
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Naruto Game"
FPS = 60

class MainScenes(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    QUIT = 3

COLORKEY = (0, 64, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GREY = (128, 128, 128)


def width_percent(val):
    return val * SCREEN_WIDTH / 100
def height_percent(val):
    return val * SCREEN_HEIGHT / 100