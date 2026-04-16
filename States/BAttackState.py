from States.Base import BaseState


class BAttackState(BaseState):
    """Basic attack (B button)"""
    def enter(self, player):
        player.animator.play("b")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        pass


class BForwardState(BaseState):
    """B attack while moving forward"""
    def enter(self, player):
        player.animator.play("b_forward")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        pass


class BUpState(BaseState):
    """B attack upward (anti-air)"""
    def enter(self, player):
        player.animator.play("b_up")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        pass


class BDownState(BaseState):
    """B attack downward"""
    def enter(self, player):
        player.animator.play("b_down")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        pass


class YAttackState(BaseState):
    """Heavy attack (Y button)"""
    def enter(self, player):
        player.animator.play("y")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        pass


class YForwardState(BaseState):
    """Y attack while moving forward"""
    def enter(self, player):
        player.animator.play("y_forward")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        pass
