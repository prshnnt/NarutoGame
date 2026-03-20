from States.Base import BaseState
from core.config import *
import pygame as pg


class RunState(BaseState):
    def enter(self, player):
        player.animator.play("run")
    def exit(self, player):
        player.velocity.x = 0

    def handle_action(self, player, action):
        if action["left"]:
            player.velocity.x = -RUN_SPEED
        elif action["right"]:
            player.velocity.x = RUN_SPEED
        else:
            player.velocity.x = 0
            if not player.in_air:
                player.change_state("idle")

        if action["space"] and not player.in_air:
            player.change_state("jump")
            return