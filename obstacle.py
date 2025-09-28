import arcade
import random

from config import *

class Obstacle:
    def __init__(self):

        self.height = random.randint(100, 500)
        self.width = random.randint(100, 300)

        self.x = SCREENWIDTH
        self.y = random.choice([0, SCREENHEIGHT - self.height])

    def update(self):
        self.x -= GAMESPEED  # Move obstacle to the left
    
    def is_off_screen(self):
        if self.x + self.width < 0:
            return True
        
    def draw(self):
        arcade.draw_lbwh_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.VIOLET)
