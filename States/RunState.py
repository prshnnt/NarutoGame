from States.Base import BaseState
from States.IdleState import IdleState
from States.JumpState import JumpState


class RunState(BaseState):

    def handle_input(self, player, keys):

        if not (keys[player.controls["left"]] or keys[player.controls["right"]]):
            player.change_state(IdleState())

        if keys[player.controls["jump"]] and player.on_ground:
            player.change_state(JumpState())

    def update(self, player, dt):

        direction = 0

        keys = player.keys

        if keys[player.controls["left"]]:
            direction = -1
        elif keys[player.controls["right"]]:
            direction = 1

        player.vel.x = direction * player.speed