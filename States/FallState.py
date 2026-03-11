from States.Base import BaseState
from States.IdleState import IdleState
from States.RunState import RunState


class FallState(BaseState):

    def update(self, player, dt):

        if player.on_ground:

            if player.vel.x != 0:
                player.change_state(RunState())
            else:
                player.change_state(IdleState())