import pygame as pg
import sys

from enum import Enum
from core.Scene import BaseScene , MenuScene
from core.config import *

class GameScenes(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    QUIT = 3

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.dt = 0
        self.active_scene = None
        self.scenes:dict[GameScenes, BaseScene] = {}


    def init(self):
        self.active_scene = GameScenes.MENU
        self.scenes[GameScenes.MENU] = MenuScene(self,self.screen)


    def on_key_down(self,key):
        if key == pg.K_ESCAPE:
            self.running = False
        self.scenes[self.active_scene].on_key_down(key)

    def on_key_pressed(self,event):
        self.scenes[self.active_scene].on_key_pressed(event)

    def update(self):
        self.scenes[self.active_scene].update(self.dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.scenes[self.active_scene].draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                self.on_key_down(event.key)
        keys = pg.key.get_pressed()
        for key in ALLOWED_KEYS:
            if keys[key]:
                self.on_key_pressed(key)


    def run(self):
        self.init()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pg.display.flip()
            self.dt = self.clock.tick(FPS)/1000
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()