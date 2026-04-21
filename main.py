import pygame as pg
from Scenes.Base import BaseScene
from Scenes.MenuScene import MenuScene
from Scenes.GameScene import GameScene
from Scenes.OptionScene import OptionScene
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
        self.action = {"left":False,"right":False,"up":False,"down":False,"b":False,"y":False,"g":False,"space":False}

    def init(self):
        self.active_scene = MainScenes.MENU
        self.scenes[MainScenes.MENU] = MenuScene(self,self.screen)
        self.scenes[MainScenes.MENU].on_enter()
        self.scenes[MainScenes.GAME] = GameScene(self,self.screen)
        self.scenes[MainScenes.OPTIONS] = OptionScene(self,self.screen)
        

    def change_scene(self, new_scene):
        self.scenes[self.active_scene].on_exit()
        self.active_scene = new_scene
        self.scenes[new_scene].on_enter()

    def update(self,dt):
        self.scenes[self.active_scene].update(dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.scenes[self.active_scene].draw()
    
    def reset_action(self):
        for key in self.action.keys():
            self.action[key] = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    return
                if event.key == pg.K_LEFT:
                    self.action["left"] = True
                elif event.key == pg.K_RIGHT:
                    self.action["right"] = True
                if event.key == pg.K_UP:
                    self.action["up"] = True
                if event.key == pg.K_DOWN:
                    self.action["down"] = True
                if event.key == pg.K_b:
                    self.action["b"] = True
                if event.key == pg.K_y:
                    self.action["y"] = True
                if event.key == pg.K_g:
                    self.action["g"] = True
                if event.key == pg.K_SPACE:
                    self.action["space"] = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.action["left"] = False
                elif event.key == pg.K_RIGHT:
                    self.action["right"] = False
                if event.key == pg.K_UP:
                    self.action["up"] = False
                if event.key == pg.K_DOWN:
                    self.action["down"] = False
                if event.key == pg.K_b:
                    self.action["b"] = False
                if event.key == pg.K_y:
                    self.action["y"] = False
                if event.key == pg.K_g:
                    self.action["g"] = False
                if event.key == pg.K_SPACE:
                    self.action["space"] = False
        
        self.scenes[self.active_scene].handle_action(self.action)

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