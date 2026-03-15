from core.GameObject import GameObject
import pygame as pg
class Text(GameObject):
    def __init__(self, x, y, text, font=None, font_size=32, color=(255, 255, 255), center=False):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.center = center
        
        if font is None:
            self.font = pg.font.Font(None, font_size)
        else:
            self.font = font
            
        self.update_surface()

    def update_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        if self.center:
            self.rect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)

    def set_text(self, new_text):
        if self.text != new_text:
            self.text = new_text
            self.update_surface()

    def draw(self, game):
        game.screen.blit(self.surface, self.rect)