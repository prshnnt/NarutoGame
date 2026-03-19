from States.Base import BaseState
from core.config import *
import pygame as pg

class JumpState(BaseState):

    def enter(self, player):
        player.animator.play("jump")
        player.velocity.y = -JUMP_FORCE
        player.in_air = True
        
    def handle_action(self, player, action):
        keys = pg.key.get_pressed()
        if keys[ALLOWED_KEYS["left"]]:
            player.velocity.x = -5
        if keys[ALLOWED_KEYS["right"]]:
            player.velocity.x = 5

    def update(self, player, dt):
        if player.velocity.y > 0:
            player.change_state("fall")