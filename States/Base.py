class BaseState:
    def enter(self,player):
        pass
    def update(self,player,dt):
        pass
    def handle_input(self,player,keys):
        pass
    def exit(self,player):
        pass