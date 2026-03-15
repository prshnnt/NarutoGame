from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    A base class for game objects.
    """
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