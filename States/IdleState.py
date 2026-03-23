from States.Base import BaseState

class IdleState(BaseState):
    def enter(self, player):
        player.animator.play("stance")
        player.velocity.x = 0
        player.velocity.y = 0
        # player.animator.just_landed = False


    def handle_action(self, player,action):
        if action["left"] or action["right"]:
            player.change_state("run")
        if action["g"]:
            player.change_state("guard")
        if action["space"] and (not player.in_air):
            player.change_state("jump")