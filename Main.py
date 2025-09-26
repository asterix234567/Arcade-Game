import arcade
import math
import random

SCREENWIDTH = 1400
SCREENHEIGHT = 800

SCREENCENTER_X = SCREENWIDTH // 2
SCREENCENTER_Y = SCREENHEIGHT // 2

# General Game Variables
GAMESPEED = 8

# Time (s) it takes for the next Obstacle to spawn 
OBSTACLESPAWNSPEED = 1

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

class Player:
    def __init__(self, rotation):
        self.center_x = SCREENCENTER_X
        self.center_y = SCREENCENTER_Y
        self.angle = rotation  # In degrees

        self.height = 45
        self.width = 50
        
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

class MyGameWindow(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREENWIDTH, SCREENHEIGHT, title)
        arcade.set_background_color(arcade.color.BABY_BLUE)

        # Create the player in __init__, not in on_draw
        self.player = Player(0)
        
        # List of all Keys that are used
        self.held_keys = set()
        
        # List of all player positions on the Screen (as tuples)
        self.positions = []
        self.max_path_length = 50  # Maximum number of positions to store

        self.obstacles = [] # List to store Obstacle objects
        self.time_since_last_obstacle = 0  # Timer to track obstacle spawning

        self.paused = False # Game paused state

            
    def on_draw(self):

        self.clear()

        if self.paused:
            arcade.draw_text("Paused", SCREENCENTER_X // 2, SCREENCENTER_Y // 2, arcade.color.BLACK, 50)
            return  # Skip drawing/updating game objects
        
        # Add new Obstacles 
        if self.time_since_last_obstacle - OBSTACLESPAWNSPEED >= 0:
            self.obstacles.append(Obstacle()) 
            self.time_since_last_obstacle = 0

        # Update and Draw Obstacles
        obstacles_to_keep = []
        for obst in self.obstacles:
            obst.update()
            obst.draw()
            self.paused = Player.obstacle_collision(self.player, obst) # Check for collision
            if self.paused:
                break  # Exit the loop if the game is paused due to a collision
            if not obst.is_off_screen():
                obstacles_to_keep.append(obst)
                
        self.obstacles = obstacles_to_keep

         # Update player path
        self.update_player_path(self.player.center_x, self.player.center_y)
        
        self.key_inputs()           # process inputs by the player 
        self.player.screen_collision ()   # check for collisions with the screen borders
        

        # Update the player's rotation
        if bool(self.player.angle):
            self.player.angle = self.get_player_rotation()
        
        # Draw the Line behind the player (only if we have positions)
        if len(self.positions) > 1:
            arcade.draw_line_strip(self.positions, arcade.color.WHITE, 8)
        
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