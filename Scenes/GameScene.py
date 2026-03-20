from Scenes.Base import BaseScene
from Components.Buttons import Button
from core import Camera , AssetLoader
from core.config import *
from core.GameObject import GameObject
# from entities.Player import Player
import pygame as pg

from entities.Player import Player

class TestPlayer(GameObject):
    def __init__(self,pos):
        self.rect = pg.Rect(pos[0],pos[1],50,50)
        self.image = pg.Surface((50,50))
        self.image.fill(YELLOW)
        self.direction = 1 # 1 for right and -1 for left
        self.vel_y = 0
        self.in_air = True
        self.speed = 5
    def update(self, scene:BaseScene,dt):
        if self.vel_y>0:
            self.color = GREEN
        elif self.vel_y<0:
            self.color = RED
        else:
            self.color = YELLOW
        self.image.fill(self.color)
        if self.in_air:
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            self.rect.y += self.vel_y
            if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                self.in_air = False
                self.vel_y = 0
            
        scene.camera.update(self.rect)
    def handle_action(self,action):
        if action["up"] and not self.in_air:
            self.in_air = True
            self.vel_y = -JUMP_FORCE
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
        self.layers = AssetLoader.load_level("assets/levels/level1.json")
        pause_button = Button(width_percent(1), height_percent(1), 50, 50, "||", None,
                              bg_color=YELLOW,
                              hover_color=PURPLE,
                              text_color=BLACK,
                              callback=lambda: self.game.change_scene(MainScenes.MENU))
        self.add_object(pause_button,"ui")
        self.world_width = AssetLoader.load_world_width("assets/levels/level1.json")

        self.camera = Camera(self.world_width,SCREEN_HEIGHT)
        self.scroll = 0
        # self.player = Player((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        self.player:Player = AssetLoader.load_player()
        
    def update(self,dt):
        for layer in  ["background", "world", "effects", "ui"]:
            for obj in self.layers[layer]:
                if obj is not self.player:
                    obj.update(self)
        self.player.update(self,dt)
        self.camera.update(self.player.rect)
    def draw(self):
        super().draw()
        self.player.draw(self)


    def handle_action(self,action):
        self.player.handle_action(action)