from States.Base import BaseState
from core.config import *
import pygame as pg

class FallState(BaseState):
    def enter(self, player):
        player.animator.play("fall")
    def exit(self, player):
        player.velocity.x = 0
    def handle_action(self, player, action):
        keys = pg.key.get_pressed()
        if keys[ALLOWED_KEYS["left"]]:
            player.velocity.x = -5
        if keys[ALLOWED_KEYS["right"]]:
            player.velocity.x = 5
