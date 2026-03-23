from Animator.Base import Animator
import pygame as pg

class NarutoAnimator(Animator):
    def __init__(self,player):
        super().__init__(player)

    def should_update_frame(self):
        current_time = pg.time.get_ticks()
        if current_time - self.prev_time < 150:
            return False
        else:
            self.prev_time = current_time
            return True
    def update_frame(self):
        if self.group == "jump":
            if self.frame_index == 0:
                self.frame_index = 1
            else:
                self.frame_index = 1
        elif self.group == "fall":
            self.frame_index = 0
        elif self.group == "guard":
            if self.frame_index == 0:
                self.frame_index = 1
            elif self.frame_index == 1:
                self.frame_index = 2
            elif self.frame_index == 2:
                self.frame_index = 2
        elif self.group == "landing":
            self.frame_index = 0
        else:
            self.frame_index += 1
            if self.frame_index >= len(self.frames[self.group]):
                self.frame_index = 0
    def update(self,dt):
        if self.group is None:
            return
        if self.should_update_frame():
            self.update_frame()

        self.image = self.frames[self.group][self.frame_index]
        self.rect_resize()