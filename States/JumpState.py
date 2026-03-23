from States.Base import BaseState
from core.config import *
import pygame as pg

class JumpState(BaseState):

    def enter(self, player):
        player.animator.play("jump")
        player.animator.frame_index = 0
        player.velocity.y = -JUMP_FORCE
        player.in_air = True
        player.animator.just_landed = False

    def exit(self, player):
        player.velocity.y = 0
        
    def handle_action(self, player, action):
        keys = pg.key.get_pressed()
        if keys[ALLOWED_KEYS["left"]]:
            player.velocity.x = -RUN_SPEED
        if keys[ALLOWED_KEYS["right"]]:
            player.velocity.x = RUN_SPEED

    def update(self, player, dt):
        if player.velocity.y > 0:
            player.change_state("fall")