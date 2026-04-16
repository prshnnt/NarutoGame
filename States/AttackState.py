class AttackState(BaseState):
    def enter(self, player):
        player.animator.play("attack")
        player.velocity.x = 0

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.change_state("idle")

    def handle_action(self, player, action):
        # Prevent movement during attack animation
        pass