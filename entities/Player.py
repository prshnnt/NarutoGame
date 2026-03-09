from enum import Enum

from core.Base import GameObject
import pygame

class PlayerState(Enum):
    STANCE = 0
    RUN = 1
    JUMP = 2
    HIT = 3
    DOWN = 4
    GUARD = 5
    B = 6
    B_FORWARD = 7
    B_UP = 8
    B_DOWN = 9
    Y = 10
    Y_FORWARD = 11
    Y_UP = 12
    DASH_ATTACK =13
    JUMP_B = 14
    JUMP_Y = 15

    
class Player:
    """
    Represents the player character.
    """

    def __init__(self,scene):
        self.scene = scene
        self.active_state = PlayerState.STANCE
        self.state = {}