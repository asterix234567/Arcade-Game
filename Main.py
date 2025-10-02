import arcade
import math
import random

from player import Player
from obstacle import Obstacle
from config import *

class MyGameWindow(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREENWIDTH, SCREENHEIGHT, title)
        arcade.set_background_color(arcade.color.BABY_BLUE)

        # Create the player
        self.player = Player(0)
        
        # List of all Keys that are used
        self.held_keys = set()
        
        # List of all player positions on the Screen (as tuples)
        self.positions = []
        self.max_path_length = 50  # Maximum number of positions to store

        self.obstacles = [] # List to store Obstacle objects
        self.time_since_last_obstacle = 0  # Timer to track obstacle spawning

        self.end_by_collision = False # Game paused state

        # Load collision animation textures
        collision_frames = []       # List of textures for death animation
        self.player.collision_animation_frames = 19      # Number of frames/files in the animation
        for i in range(1, self.player.collision_animation_frames):              
            texture = arcade.load_texture(f"textures/Player/collision_animation/Blue Ring Explosion{i}.png")
            collision_frames.append(texture)
        self.player.collision_animation_textures = collision_frames      # Assign the loaded textures to the player

        #Load player texture
        self.texture = arcade.load_texture("textures/Player/plane.png")
        self.player.texture = self.texture

        #Load obstacle texture
        self.obstacle_texture = arcade.load_texture("textures/Obstacle/building.png")

            
    def on_draw(self):

        self.clear()

        if self.end_by_collision:
            
            if self.player.collision_animation_index == self.player.death_animation_frames:       # If the animation is done, pause the game
                arcade.draw_text("Paused", SCREENCENTER_X // 2, SCREENCENTER_Y // 2, arcade.color.BLACK, 50)
            else:
                arcade.draw_line_strip(self.positions, arcade.color.WHITE, 8)
                for obst in self.obstacles:
                    obst.draw()         # Draw the obstacle

                Player.collision_animation(self.player) # Show collision animation
            
            return  # Skip drawing/updating game objects
        
        else:
            # Add new Obstacles 
            if self.time_since_last_obstacle - OBSTACLESPAWNSPEED >= 0:
                self.obstacles.append(Obstacle(self.obstacle_texture)) 
                self.time_since_last_obstacle = 0

            # Update and Draw Obstacles
            obstacles_to_keep = []
            for obst in self.obstacles:
                obst.update()       # Move the obstacle to the left
                obst.draw()         # Draw the obstacle
                if not obst.is_off_screen():
                    obstacles_to_keep.append(obst)

                self.end_by_collision = Player.obstacle_collision(self.player, obst) # Check for collision
                if self.end_by_collision:
                    break  # Exit the loop if the game is paused due to a collision

                
                self.obstacles = obstacles_to_keep

            # Update player path
            self.update_player_path(self.player.center_x, self.player.center_y)
        
            self.key_inputs()           # process inputs by the player 
            self.player.screen_collision ()   # check for collisions with the screen borders
        

            # Update the player's rotation
            if bool(self.player.angle):
                self.player.angle = self.get_player_rotation()
            print(self.player.angle)
        
            # Draw the Line behind the player (only if we have positions)
            if len(self.positions) > 1:
                arcade.draw_line_strip(self.positions, arcade.color.WHITE, 8)
        
            # Update the player hitbox
            self.player.update_hitbox()

            # Draw the player
            self.player.draw()

    def update_player_path(self, x, y):
        # Add current position as a tuple
        self.positions.append((x, y))
        
        for i in range(len(self.positions)):
            x, y = self.positions[i]
            self.positions[i] = (x - GAMESPEED, y)
             
        # Limit the length of the path
        if self.positions[0][0] <= 0:
            self.positions.pop(0)  # Remove oldest position
    
    def get_player_rotation(self):
        # Determine rotation based on movement direction
        if arcade.key.W in self.held_keys or "left_mouse_button" in self.held_keys:
            return 45  # Upward
        else:
            return -45  # Downward
    
    def on_key_press(self, key, modifiers):
        self.held_keys.add(key)             # add the last key that was pressed to the current pressed keys
        
    def on_key_release(self, key, modifiers):
        if key in self.held_keys:   
            self.held_keys.remove(key)       # removes the last released key from the current pressed keys
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.held_keys.add("left_mouse_button")
        
    def on_mouse_release(self, x, y, button, modifiers):
        if "left_mouse_button" in self.held_keys:
            self.held_keys.remove("left_mouse_button")
        
    def key_inputs(self):
        # Moves the player if the W-key is pressed
        if arcade.key.W in self.held_keys or "left_mouse_button" in self.held_keys:
            self.player.center_y += GAMESPEED
        else:
            self.player.center_y -= GAMESPEED
    
    def on_update(self, delta_time):
        delta_time # time since last update in seconds.

        self.time_since_last_obstacle += delta_time


def main():
    window = MyGameWindow("SpaceWaves")
    arcade.run()
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Game crashed: {e}")
    finally:
        print("Worked")