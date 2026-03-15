from Components import ParallaxBackground
from Scenes.Base import BaseScene
from Components.Buttons import Button
from core import Camera , AssetLoader
from core.config import *
from core.GameObject import GameObject
# from entities.Player import Player
import pygame as pg

class Player(GameObject):
    def __init__(self,pos):
        self.rect = pg.Rect(pos[0],pos[1],50,50)
        self.image = pg.Surface((50,50))
        self.image.fill(YELLOW)
        self.direction = 1 # 1 for right and -1 for left
        self.speed = 5
    def update(self, scene:BaseScene):
        
    def handle_event(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    def draw(self, scene:BaseScene):
        scene.screen.blit(self.image,scene.camera.apply(self.rect))


class GameScene(BaseScene):
    def on_enter(self):
        pause_button = Button(width_percent(1), height_percent(1), 50, 50, "||", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.MENU))
        self.add_object(pause_button,"ui")
        self.layers = AssetLoader.load_level("assets/levels/level1.json")
        self.world_width = AssetLoader.load_world_width("assets/levels/level1.json")

        self.camera = Camera(self.world_width,SCREEN_HEIGHT)
        self.scroll = 0
        self.player = Player((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        self.add_object(self.player,"world")
        # self.player = Player((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
    def update(self,dt):
        super().update(dt)
        self.player.handle_event()
        self.player.update(self)
        self.camera.update(self.player.rect)