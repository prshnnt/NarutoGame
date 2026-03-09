from enum import Enum
import pygame as pg



class State:
    def __init__(self,screen:pg.Surface,objects=[]):
        self.screen = screen
        self.objects = objects
    def add_object(self,obj):
        self.objects.append(obj)
    def remove_object(self,obj):
        self.objects.remove(obj)
    def update(self,dt,events,mouse_pos):
        for obj in self.objects:
            obj.update(dt,events,mouse_pos)
    def draw(self):
        for obj in self.objects:
            obj.draw(self.screen)
class MenuState(State):
    class MenuStates(Enum):
        MENU = 0
        START = 1
        OPTION = 2
        EXIT = 3
    def __init__(self,screen:pg.Surface):
        super().__init__(screen)
        self.load_layout()

class MainState:
    class MainStates(Enum):
        MENU = 0
        PLAYING = 1
        PAUSED = 2
        GAME_OVER = 3
        OPTIONS = 4
        CREDITS = 5
        QUIT = 6
        
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.current_state = self.GameStates.PLAYING
        self.states = {
            self.GameStates.PLAYING: State(screen),
            self.GameStates.PAUSED: State(screen),
            self.GameStates.GAME_OVER: State(screen)
        }
        
    def update(self, dt, events, mouse_pos):
        if self.current_state in self.states:
            self.states[self.current_state].update(dt, events, mouse_pos)

    def draw(self):
        if self.current_state in self.states:
            self.states[self.current_state].draw()

    def change_state(self, state):
        if state in self.states:
            self.current_state = state