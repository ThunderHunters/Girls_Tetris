# Girls Tetris Main

# Import necessary modules and classes
from Settings import *
from Girls_Tetris_Game import Tetris, Text 
import sys 
import pathlib

# Define the main application class
class App:
    def __init__(self):
        # Initialize Pygame
        pg.init()
        # Set the window caption
        pg.display.set_caption("Tetris for Girls")
        # Create the game window
        self.screen = pg.display.set_mode(WIN_RES)
        # Initialize the game clock for controlling the frame rate
        self.clock = pg.time.Clock()
        # Set up timer events for animation
        self.set_timer()
        # Load images used in the game
        self.images = self.load_images()
        # Create an instance of the Tetris game and Text classes
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.sprite_group = pg.sprite.Group()

    # Load images from the specified directory
    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob("*.png") if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images
                                                                   
    # Set up timer events for animation
    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    # Update game state
    def update(self):
        # Check if animation trigger is active and update the Tetris game
        if self.anim_trigger:
            self.tetris.update()
        # Update sprite group (ensure it is initialized elsewhere)
        self.sprite_group.update()

    # Draw the game window
    def draw(self):
        # Fill the screen with the specified color
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw() 
                         
        # Update the display
        pg.display.flip()

    # Check for and handle user events
    def check_events(self):
        # Reset animation triggers
        self.anim_trigger = False
        self.fast_anim_trigger = False
        # Check Pygame events
        for event in pg.event.get():
            # Quit the game if the window is closed or 'ESC' is pressed
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            # Pass the pressed key to the Tetris control method if a key is pressed
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            # Set animation trigger when user event timer is triggered
            elif event.type == self.user_event:
                self.anim_trigger = True
            # Set fast animation trigger when fast user event timer is triggered
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True  


                                            

    # Main game loop
    def run(self):
        while True:
            # Check for user events
            self.check_events()
            # Update game state
            self.update()
            # Draw the game window
            self.draw()




# Entry point of the program
if __name__ == "__main__":
    # Create an instance of the App class and run the game loop
    app = App()
    app.run()
