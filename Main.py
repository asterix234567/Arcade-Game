import arcade
import math

SCREENWIDTH = 1400
SCREENHEIGHT = 800

SCREENCENTER_X = SCREENWIDTH // 2
SCREENCENTER_Y = SCREENHEIGHT // 2

# Player 
player_width = 50
player_height = 45
PLAYERSPEED = 5

class Player:
    def __init__(self, rotation):
        self.center_x = SCREENCENTER_X
        self.center_y = SCREENCENTER_Y
        self.angle = rotation  # In degrees
        
    def draw(self):
        # Calculate the rotated points of the triangle
        angle_rad = math.radians(self.angle)
        cos_val = math.cos(angle_rad)
        sin_val = math.sin(angle_rad)
        
        # Original triangle points (relative to center)
        points = [
            [-player_width // 2, -player_height // 2],  # Bottom-left
            [-player_width // 2, player_height // 2],   # Top-left
            [player_width // 2, 0]                      # Right
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
            
    def on_draw(self):
        self.clear()
        
         # Update player path
        self.update_player_path(self.player.center_x, self.player.center_y)
        
        self.key_inputs()           # process inputs by the player 
        self.player_collision()
        
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
            self.positions[i] = (x - PLAYERSPEED, y)
             
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
            self.player.center_y += PLAYERSPEED
        else:
            self.player.center_y -= PLAYERSPEED

    def player_collision(self):
        # Top and Bottom Coordinate - Same as in draw Player: Same Same, but different
        if self.player.center_y + player_height // 2 > SCREENHEIGHT:
            self.player.center_y = SCREENHEIGHT - player_height // 2
            
            self.player.angle = 0
        
        elif self.player.center_y - player_height // 2 < 0:
            self.player.center_y = 0 + player_height // 2
            
            self.player.angle = 0

        else:
            self.player.angle = 1
    
    def on_update(self, delta_time):
        # Here you can implement additional updates
        pass

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