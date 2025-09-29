import arcade
import math

from config import *


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Player:
    def __init__(self, rotation):
        self.center_x = SCREENCENTER_X
        self.center_y = SCREENCENTER_Y
        self.angle = rotation  # In degrees

        self.height = 45
        self.width = 50

        self.death_animation_frames = 60  #Width of the Death Circle = player.width // death_animation_frames
        self.death_current_frame = 0 

        self.collision_animation_textures = []       # List of textures for death animation
        for i in range(1, 19):                        # Number of frames in the animation
            texture = arcade.load_texture(f"Player_collision_animation/Blue Ring Explosion{i}.png")
            self.collision_animation_textures.append(texture)
        self.collision_animation_index = 0      # Current frame in the collision animation

        self.collision_animation_size = 4 # Size multiplier for the collision animation - size of the player * animation_size
        

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
    
    def collision_animation(self): # Draw expanding red circle
        
        # # For faster Expansion change the multiplier of death_current_frame
        # circle_radius = self.death_animation_frames * (1 - math.e**(-1 *(0.02 * self.death_current_frame)))
        # arcade.draw_circle_filled(self.center_x, self.center_y, circle_radius, arcade.color.RED)
        
        # self.death_current_frame += 1

        #collision_animation_rect = arcade.rect(400, 400, 400, 400)
        #collision_animation_rect = arcade.Rect.(self.center_x, self.center_y, self.width, self.height)
        #collision_animation_rect = arcade.Rect.__new__(self.width, self.height, self.center_x, self.center_y)
        if len(self.collision_animation_textures) - self.collision_animation_index:
            self.collision_animation_rect = Rect(self.center_x, self.center_y, self.width * self.collision_animation_size, self.height * self.collision_animation_size)

        if self.collision_animation_index <= len(self.collision_animation_textures):
            #collision_animation_rect = arcade.Rect(self.width, self.height, self.center_x, self.center_y)
            arcade.draw_texture_rect(self.collision_animation_textures[self.collision_animation_index], self.collision_animation_rect)
            self.collision_animation_index += 1