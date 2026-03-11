import pygame as pg

from core.GameObject import GameObject

class Button(GameObject):
    def __init__(self, x, y, width, height, text, font, bg_color=(200, 200, 200), hover_color=(150, 150, 150), text_color=(0, 0, 0), callback=None, choice = None):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        if font is None:
            self.font = pg.font.Font(None, 32)
        else:
            self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.choice = choice
        self.toggled = False
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                if self.callback:
                    self.callback()

    def update(self, dt):
        pass
    def set_text(self, text):
        self.text = text
    def toggle_choice(self):
        if self.choice is not None:
            if self.toggled:
                self.toggled = False
                self.text = self.choice[0]
            else:
                self.toggled = True
                self.text = self.choice[1]



    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.bg_color
        pg.draw.rect(screen, color, self.rect)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)