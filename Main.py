import arcade
import math

SCREENWIDTH = 1400
SCREEN_HEIGHT = 800

SCREENCENTER_X = SCREENWIDTH // 2
SCREENCENTER_Y = SCREEN_HEIGHT // 2

# Player 
player_width = 40
player_height = 35
PLAYERSPEED = 8

class Player:
    def __init__(self, center_x, center_y, rotation):
        self.center_x = center_x
        self.center_y = center_y
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
        super().__init__(SCREENWIDTH, SCREEN_HEIGHT, title)
        arcade.set_background_color(arcade.color.BABY_BLUE)

        # Create the player in __init__, not in on_draw
        self.player = Player(SCREENCENTER_X, SCREENCENTER_Y, 0)
        
        # List of all Keys that are used
        self.held_keys = set()
            
    def on_draw(self):
        self.clear()
        
        self.key_inputs()           # process inputs by the player 
        self.player_collision()
        
        # Update the player's rotation
        if bool(self.player.angle):
            self.player.angle = self.get_player_rotation()
        
        # Draw the player
        self.player.draw()
    
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
        if self.player.center_y + player_height // 2 > SCREEN_HEIGHT:
            self.player.center_y = SCREEN_HEIGHT - player_height // 2
            
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