import pygame
from enum import Enum


SCREEN_WIDTH:int = 960
SCREEN_HEIGHT:int = 500
GROUND_HEIGHT:int = 50
RUN_SPEED = SCROLL_SPEED = 3
PLAYER_SPEED = 10
JUMP_FORCE = 15
GRAVITY = 0.5
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Naruto Game"
FPS = 60

TILE_SIZE = (50,50)

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

ALLOWED_KEYS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "b": pygame.K_b,
    "y": pygame.K_y,
    "g": pygame.K_g,
    "space": pygame.K_SPACE
}

def width_percent(val):
    return val * SCREEN_WIDTH / 100
def height_percent(val):
    return val * SCREEN_HEIGHT / 100