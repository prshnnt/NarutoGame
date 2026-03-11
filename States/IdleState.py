from States.Base import BaseState
from States.RunState import RunState
from States.JumpState import JumpState


class IdleState(BaseState):

    def enter(self, player):
        pass

    def handle_input(self, player, keys):

        if keys[player.controls["left"]] or keys[player.controls["right"]]:
            player.change_state(RunState())

        if keys[player.controls["jump"]] and player.on_ground:
            player.change_state(JumpState())