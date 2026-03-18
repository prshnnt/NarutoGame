class BaseState:
    def enter(self,player):
        pass
    def exit(self,player):
        pass
    def handle_input(self,player,keys):
        pass
    def update(self,player,dt):
        pass
    def draw(self,player,screen):
        pass