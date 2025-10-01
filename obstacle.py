import arcade
import random

from config import *

class Rect():

    def __init__(self):
        self.x = 0
        self.y =  0
        self.width = 0
        self.height = 0

    def update(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Obstacle:
    def __init__(self, texture):

        self.height = random.randint(100, 500)
        self.width = random.randint(100, 300)

        self.x = SCREENWIDTH
        self.y = random.choice([0, SCREENHEIGHT - self.height])

        self.center_x = self.x + self.width // 2
        self.center_y = self.y + self.height // 2

        self.rect = Rect()

        self.texture = texture  

    def update(self):
        self.x -= GAMESPEED  # Move obstacle to the left
    
    def is_off_screen(self):
        if self.x + self.width < 0:
            return True
        
    def draw(self):
        # Draw the obstacle with the updated rectangle
        self.rect.update(self.x + self.width // 2, self.y + self.height // 2, self.width, self.height)
        arcade.draw_texture_rect(self.texture, self.rect)
