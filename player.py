import arcade
import math

from config import *


class Player:
    def __init__(self, rotation):
        self.center_x = SCREENCENTER_X
        self.center_y = SCREENCENTER_Y
        self.angle = rotation  # In degrees

        self.height = 45
        self.width = 50

        self.death_animation_frames = 80  #Width of the Death Circle = player.width // death_animation_frames
        self.death_current_frame = 0 
        
    def draw(self):
        # Calculate the rotated points of the triangle
        angle_rad = math.radians(self.angle)
        cos_val = math.cos(angle_rad)
        sin_val = math.sin(angle_rad)
        
        # Original triangle points (relative to center)
        points = [
            [-self.width // 2, -self.height // 2],  # Bottom-left
            [-self.width // 2, self.height // 2],   # Top-left
            [self.width // 2, 0]                      # Right
        ]
        
        # Rotate and translate the points
        rotated_points = []
        for x, y in points:
            # Apply rotation
            rotated_x = x * cos_val - y * sin_val
            rotated_y = x * sin_val + y * cos_val
            
            # Translate to center position
            rotated_points.append((rotated_x + self.center_x, rotated_y + self.center_y))
        
        # Draw the rotated triangle
        arcade.draw_polygon_filled(rotated_points, arcade.color.BLACK)

    def screen_collision(self):
        # Top and Bottom Coordinate - Same as in draw Player: Same Same, but different
        if self.center_y + self.height // 2 > SCREENHEIGHT:
            self.center_y = SCREENHEIGHT - self.height // 2
            
            self.angle = 0
        
        elif self.center_y - self.height // 2 < 0:
            self.center_y = 0 + self.height // 2
            
            self.angle = 0

        else:
            self.angle = 1

    def obstacle_collision(self, obstacle):
        # Check for collision with an obstacle
        if (self.center_x + self.width // 2 > obstacle.x and
            self.center_x - self.width // 2 < obstacle.x + obstacle.width and
            self.center_y + self.height // 2 > obstacle.y and
            self.center_y - self.height // 2 < obstacle.y + obstacle.height):
            return True
        return False
    
    def collision_animation(self):

        circle_radius = self.death_animation_frames * (1 - math.e**(-1 *(0.01 * self.death_current_frame)))
        arcade.draw_circle_filled(self.center_x, self.center_y, circle_radius, arcade.color.RED)
        #circle_radius = 10 + 40 * math.log1p(self.death_current_frame)
        #arcade.draw_circle_filled(self.center_x, self.center_y, circle_radius, arcade.color.RED)
        self.death_current_frame += 1