class BaseState:
    def enter(self,player):
        pass
    def exit(self,player):
        pass
    def handle_action(self,player,action):
        pass
    def update(self,player,dt):
        pass