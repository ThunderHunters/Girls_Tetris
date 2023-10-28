# Girls Tetris Game

# Import necessary modules and classes
from Settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft
import pygame as pg
from Music import play_background_music, play_score_sound



### Replace X with custom file path on your computer.###
FONT_PATH = "XBradley Hand Bold.ttf"

tetris_text = 'TETRIS'
next_text = 'NEXT'
score_text = 'SCORE'


play_background_music()

# Define the Text class for displaying game-related text
class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    # Function to get a dynamic color for text
    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    # Function to draw various text elements on the screen
    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.62, WIN_H * 0.016),
                            text='GIRLS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.85)


        self.font.render_to(self.app.screen, (WIN_W * 0.6, WIN_H * 0.095),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.85)
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.28),
                            text='NEXT', fgcolor='white',
                            size=TILE_SIZE * 1.7,)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.72),
                            text='SCORE',  fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.74, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='red',
                            size=TILE_SIZE * 1.8)

   


    # Underline specific words
        underline_size = TILE_SIZE * 0.15

    # Underline "TETRIS"
        underline_rect = pg.Rect((WIN_W * 0.6, WIN_H * 0.065 + TILE_SIZE * 1.85), 
                             (self.font.get_rect(tetris_text, size=TILE_SIZE * 1.85)[2], underline_size))
        pg.draw.rect(self.app.screen, self.get_color(), underline_rect)

    # Underline "SCORE"
        underline_rect = pg.Rect((WIN_W * 0.64, WIN_H * 0.70 + TILE_SIZE * 1.4),
                             (self.font.get_rect(score_text, size=TILE_SIZE * 1.4)[2], underline_size))
        pg.draw.rect(self.app.screen, self.get_color(), underline_rect)

# Define the Tetris class for handling the game logic
class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        self.next_pos_offset = NEXT_POS_OFFSET

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

        # Initialize sprite_index
        self.sprite_index = 0

    # Function to update the score based on completed lines
    def get_score(self):
        previous_score = self.score
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

        # Play score sound when the score changes
        if self.score != previous_score:
            play_score_sound()       

    

    # Function to check and clear full lines in the game field
    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
 
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1



    # Function to place the blocks of the current tetromino in the game field array
    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    # Function to initialize the game field array
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    # Function to check if the game is over
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    # Function to check if the current tetromino has landed
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
                     
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    # Function to handle player controls
    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.tetromino.move(direction="down", speed_multiplier=1)  # Adjust the speed multiplier as needed

    # Function to draw the game grid
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, "black",
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # Function to update the game state
    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    # Function to draw the game elements
    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
