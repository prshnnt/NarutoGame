from abc import ABC, abstractmethod
import pygame as pg

class GameObject(ABC):
    """
    A base class for game objects.
    """
    rect: pg.Rect
    image: pg.Surface

    def handle_action(self,action):
        pass
    @abstractmethod
    def update(self, scene):
        """
        Updates the game object's state. This method is called once per frame.
        """
        pass
    @abstractmethod
    def draw(self, scene):
        """
         Draws the game object to the screen.
        """
        pass