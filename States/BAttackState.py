from States.Base import BaseState


class BAttackState(BaseState):
    """Basic attack (B button)"""
    def enter(self, player):
        player.animator.play("b")
        player.velocity.x = 0
        player.create_hitbox(width=40, height=30)

    def update(self, player, dt):
        if player.animator.animation_finished:
            # Only Player has attack_queue
            if hasattr(player, 'attack_queue') and player.attack_queue:
                player.process_next_attack()
            else:
                player.change_state("idle")

    def handle_action(self, player, action):
        pass


class BForwardState(BaseState):
    """B attack while moving forward"""
    def enter(self, player):
        player.animator.play("b_forward")
        player.velocity.x = 0
        player.create_hitbox(width=50, height=30)

    def update(self, player, dt):
        if player.animator.animation_finished:
            # Only Player has attack_queue
            if hasattr(player, 'attack_queue') and player.attack_queue:
                player.process_next_attack()
            else:
                player.change_state("idle")

    def handle_action(self, player, action):
        pass


class BUpState(BaseState):
    """B attack upward (anti-air)"""
    def enter(self, player):
        player.animator.play("b_up")
        player.velocity.x = 0
        player.create_hitbox(width=40, height=50, offset_x=-10)

    def update(self, player, dt):
        if player.animator.animation_finished:
            # Only Player has attack_queue
            if hasattr(player, 'attack_queue') and player.attack_queue:
                player.process_next_attack()
            else:
                player.change_state("idle")

    def handle_action(self, player, action):
        pass


class BDownState(BaseState):
    """B attack downward"""
    def enter(self, player):
        player.animator.play("b_down")
        player.velocity.x = 0
        player.create_hitbox(width=40, height=20)

    def update(self, player, dt):
        if player.animator.animation_finished:
            # Only Player has attack_queue
            if hasattr(player, 'attack_queue') and player.attack_queue:
                player.process_next_attack()
            else:
                player.change_state("idle")

    def handle_action(self, player, action):
        pass


class YAttackState(BaseState):
    """Heavy attack (Y button) - higher damage"""
    def enter(self, player):
        player.animator.play("y")
        player.velocity.x = 0
        player.create_hitbox(width=60, height=40)
        player.attack_damage = 20

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.attack_damage = 10
            player.change_state("idle")

    def handle_action(self, player, action):
        pass


class YForwardState(BaseState):
    """Y attack while moving forward - higher damage"""
    def enter(self, player):
        player.animator.play("y_forward")
        player.velocity.x = 0
        player.create_hitbox(width=70, height=40)
        player.attack_damage = 20

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.attack_damage = 10
            player.change_state("idle")

    def handle_action(self, player, action):
        pass
