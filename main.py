from cmath import e

import pygame as pg
import sys

from enum import Enum
from Scenes.Base import BaseScene
from Scenes.MenuScene import MenuScene
from Scenes.GameScene import GameScene
from core.config import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(WINDOW_TITLE)
        self.clock = pg.time.Clock()

        self.running = True
        
        self.active_scene = None
        self.scenes:dict[MainScenes, BaseScene] = {}


    def init(self):
        self.active_scene = MainScenes.MENU
        self.scenes[MainScenes.MENU] = MenuScene(self,self.screen)
        self.scenes[MainScenes.MENU].on_enter()
        self.scenes[MainScenes.GAME] = GameScene(self,self.screen)

    def change_scene(self, new_scene):
        self.scenes[self.active_scene].on_exit()
        self.active_scene = new_scene
        # if new_scene not in self.scenes:
        #     self.scenes[new_scene] = create_scene()
        self.scenes[new_scene].on_enter()

    def update(self,dt):
        self.scenes[self.active_scene].update(dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.scenes[self.active_scene].draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    return
            self.scenes[self.active_scene].handle_event(event)

    def run(self):
        self.init()

        while self.running:
            dt = self.clock.tick(FPS)/1000
            self.handle_events()
            self.update(dt)
            self.draw()
            pg.display.flip()
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()