import arcade

SCREENWIDTH = 1400
SCREEN_HEIGHT = 800

WINDOWCENTER_X = SCREENWIDTH // 2
WINDOWCENTER_Y = SCREEN_HEIGHT // 2

#Player 
player_width = 40
player_height = 35
PLAYERSPEED = 5

    
def draw_player(center_x, center_y):
        #Top-Coordinate
        x1 = center_x - player_width // 2
        y1 = center_y + player_height // 2
        
        #Right Coordinate
        x2 = center_x + player_width // 2     
        y2 = center_y
        
        #Bottom-Coordinate
        x3 = center_x - player_width // 2
        y3 = center_y - player_height // 2
        
        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color.BLACK)


class MyGameWindow(arcade.Window):
    def __init__(self, title):
        super().__init__(SCREENWIDTH, SCREEN_HEIGHT, title)
        arcade.set_background_color(arcade.color.BABY_BLUE)

        #Player Center Coordinates
        self.player_x = WINDOWCENTER_X
        self.player_y = WINDOWCENTER_Y
        
        #List of all Keys that are used
        self.held_keys = set()
        
    def on_draw(self):
        self.clear()
                    
        #Drawing the Players Triangle
        draw_player(self.player_x, self.player_y)
    
    def on_key_press(self, key, modifiers):
        # add the last key that was pressed to the current pressed keys
        self.held_keys.add(key)
        
    def on_key_release(self, key, modifiers):
        # removes the last released key from the current pressed keys
        if key in self.held_keys:
            self.held_keys.remove(key)
        
    def on_update(self, delta_time):
        # Moves the player if the key is still pressed
        if arcade.key.W in self.held_keys:
            self.player_y += PLAYERSPEED            

def main():
    window = MyGameWindow("SpaceWaves")
    arcade.run()
    
if __name__ == "__main__":
    main()