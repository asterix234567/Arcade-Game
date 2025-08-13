import arcade

# Fenster-Konstanten
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mein erstes Arcade-Fenster"

class MyGame(arcade.Window):
    """
    Hauptklasse für das Spiel.
    """
    def __init__(self, width, height, title):
        # Ruft den Konstruktor der Elternklasse auf
        super().__init__(width, height, title)

        # Setzt die Hintergrundfarbe
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Wird aufgerufen, wenn das Fenster neu gezeichnet werden muss.
        """
        # Löscht den Bildschirm mit der eingestellten Hintergrundfarbe
        # Dies ersetzt arcade.start_render()
        self.clear() 

        # Zeichne einen blauen Kreis in der Mitte des Fensters
        arcade.draw_circle_filled(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 50, arcade.color.BLUE
        )

def main():
    """
    Hauptfunktion des Programms.
    """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()