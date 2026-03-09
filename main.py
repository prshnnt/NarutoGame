import pygame as pg
from core.EventHandler import KeyBoardEventHandler
from core.State import State
from core.config import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption(WINDOW_TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.keyboardevents = KeyBoardEventHandler()
        # self.state = State()


    def init(self):
        self.keyboardevents.register('keydown', self.on_key_down)
        self.keyboardevents.register('on_key_pressed', self.on_key_pressed)
        self.keyboardevents.register('quit', self.on_quit)

    def on_key_down(self,key):
        if key == pg.K_ESCAPE:
            self.running = False
    def on_key_pressed(self,event):
        pass
    def on_quit(self):
        self.running = False

    def update(self):
        pass

    def draw(self):
        pass

    def handle_events(self):
        self.keyboardevents.handle_events()
        self.keyboardevents.handle_pressed()

    def run(self):
        self.init()

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()

if __name__ == "__main__":
    game = Game()
    game.run()