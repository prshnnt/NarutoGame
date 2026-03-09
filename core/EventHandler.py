import pygame

class KeyBoardEventHandler:
    def __init__(self):
        self._listeners = {
            'keydown':[],
            'on_key_pressed':[],
            'quit':[]
        }

    def register(self, event_name, callback):
        if event_name in self._listeners:
            self._listeners[event_name].append(callback)
        else:
            raise ValueError(f"Invalid event name: {event_name}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for callback in self._listeners['quit']:
                    callback()
            if event.type == pygame.KEYDOWN:
                for callback in self._listeners['keydown']:
                    callback(event.key)

    def handle_pressed(self):
        keys = pygame.key.get_pressed()
        for callback in self._listeners['on_key_pressed']:
            callback(keys)