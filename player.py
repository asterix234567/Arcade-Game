import arcade
import math

from config import *


class Rect:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

class rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Player:
    def __init__(self, rotation):
        self.center_x = SCREENCENTER_X
        self.center_y = SCREENCENTER_Y
        self.angle = 0  # In degrees

        self.height = 40
        self.width = 70

        self.collision_animation_textures = []       # List of textures for death animation
        self.collision_animation_index = 0      # Current frame in the collision animation
        self.collision_animation_size = 4 # Size multiplier for the collision animation - size of the player * animation_size
        self.collision_animation_frames = 0      # Number of frames in the death animation

        self.texture = 0  # Placeholder for player texture
        self.texture_corners = []  # List to hold the corner points of the texture
        self.texture_rotated_corners = []  # List to hold the rotated corner points
        self.texture_rect = Rect() # Rectangle for texture drawing
        

    def update_hitbox(self):

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
        #arcade.draw_polygon_filled(rotated_points, arcade.color.BLACK)

    def draw(self):
        
        

        # Draw the texture using the rotated corners
        arcade.draw_texture_rect(self.texture, self.texture_rect)

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
    
    def collision_animation(self): # Draw expanding red circle
        
        if len(self.collision_animation_textures) - self.collision_animation_index:
            self.collision_animation_rect = Rect(self.center_x, self.center_y, self.width * self.collision_animation_size, self.height * self.collision_animation_size)

        if self.collision_animation_index < len(self.collision_animation_textures):
            # Draw the current frame of the collision animation with the updated rectangle
            arcade.draw_texture_rect(self.collision_animation_textures[self.collision_animation_index], self.collision_animation_rect)
            self.collision_animation_index += 1
