from States.Base import BaseState


class HitState(BaseState):
    """Hit reaction state - entered when player is hit during attack or normal state."""
    def enter(self, player):
        player.animator.play("hit")
        player.velocity.x = -player.facing * 2  # Knockback
        player.invincible = True

    def update(self, player, dt):
        if player.animator.animation_finished:
            player.invincible = False
            player.velocity.x = 0
            player.change_state("idle")

    def handle_action(self, player, action):
        # No actions allowed during hit reaction
        pass
