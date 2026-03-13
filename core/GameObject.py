from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    A base class for game objects.
    """
    def handle_event(self,event):
        pass
    @abstractmethod
    def update(self, dt):
        """
        Updates the game object's state. This method is called once per frame.
        'dt' is the time in seconds since the last frame.
        """
        pass
    @abstractmethod
    def draw(self, screen):
        """
         Draws the game object to the screen.
        """
        pass