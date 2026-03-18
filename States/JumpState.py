from States.Base import BaseState

class JumpState(BaseState):

    def enter(self, player):
        player.vel.y = -player.jump_force
        player.on_ground = False

    def update(self, player, dt):
        from States import FallState
        if player.vel.y > 0:
            player.change_state(FallState())