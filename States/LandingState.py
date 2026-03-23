from States.Base import BaseState
import pygame as pg

class LandingState(BaseState):
    def __init__(self):
        self.enter_time = 0

    def enter(self, player):
        player.animator.play("landing")
        self.enter_time = pg.time.get_ticks()

    def update(self, player, dt):
        # Wait for a short duration to show the landing animation
        if pg.time.get_ticks() - self.enter_time > 200:
            player.change_state("idle")

    def handle_action(self, player, action):
        # Ignore input during landing
        pass
