import arcade

SCREENWIDTH = 1400
SCREEN_HEIGHT = 800

SCREENCENTER_X = SCREENWIDTH // 2
SCREENCENTER_Y = SCREEN_HEIGHT // 2

#Player 
player_width = 40
player_height = 35
PLAYERSPEED = 8

    
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
        self.player_x = SCREENCENTER_X
        self.player_y = SCREENCENTER_Y
        
        #List of all Keys that are used
        self.held_keys = set()
        
    def on_draw(self):
        self.clear()
        
        # process inputs by the player
        self.key_inputs()   
                   
        self.player_collision()               
        #Drawing the Players Triangle
        draw_player(self.player_x, self.player_y)
    
    def on_key_press(self, key, modifiers):
        # add the last key that was pressed to the current pressed keys
        self.held_keys.add(key)
        
    def on_key_release(self, key, modifiers):
        # removes the last released key from the current pressed keys
        if key in self.held_keys:
            self.held_keys.remove(key)
    
    def player_collision(self):
        #Top and Bottom Coordinate - Same as in draw Player: Same Same, but different
        if self.player_y + player_height // 2 > SCREEN_HEIGHT:
            self.player_y = SCREEN_HEIGHT - player_height // 2
        elif self.player_y - player_height // 2 < 0:
            self.player_y = 0 + player_height // 2
       
    def key_inputs(self):
        # Moves the player if the W-key is pressed
        if arcade.key.W in self.held_keys:
            self.player_y += PLAYERSPEED
        else:
            self.player_y -= PLAYERSPEED

                
    #def on_update(self, delta_time):
        
        
        
        
                

def main():
    window = MyGameWindow("SpaceWaves")
    arcade.run()
    
if __name__ == "__main__":
    main()