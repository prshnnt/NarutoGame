from States.Base import BaseState
from States.FallState import FallState


class JumpState(BaseState):

    def enter(self, player):
        player.vel.y = -player.jump_force
        player.on_ground = False

    def update(self, player, dt):

        if player.vel.y > 0:
            player.change_state(FallState())