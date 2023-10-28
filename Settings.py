# exampleSettings

# Import Pygame module
import pygame as pg

# Initialize Pygame
pg.init()

# Define a 2D vector class
vec = pg.math.Vector2

# Frames per second
FPS = 60
FIELD_COLOR = (48, 39, 32)
BG_COLOR = (21, 197, 255)  

# Color of the game field
FIELD_COLOR = (48, 39, 32)

# Path to the folder containing sprite images (customize for your computer)
SPRITE_DIR_PATH = "/Users/acapol200/Documents/Angela Capolino Docs/2023 SAVE FOLDER/mac python projects"

# Time interval for regular animation (in milliseconds)
ANIM_TIME_INTERVAL = 200

# Time interval for fast animation (in milliseconds)
FAST_ANIM_TIME_INTERVAL = 15

# Size of each tile in pixels
TILE_SIZE = 40

# Size of the game field (width, height)
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20

# Resolution of the game window
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

#FIELD_RES = (FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE)
WIN_RES = (FIELD_RES[1] + 500, FIELD_RES[1])  # Increase the width for additional space

# Scaling factors for the game window
FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

# Initial position offset for tetrominos
INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET  = vec(FIELD_W * 1.3, FIELD_H * 0.45)

# Dictionary defining move directions for tetrominos
MOVE_DIRECTIONS = {"left": vec(-1, 0), "right": vec(1, 0), "down": vec(0, 1)}

# Dictionary defining the shape of each tetromino
TETROMINOS = {
    "T": [(0, 0), (-1, 0), (1, 0), (0, -1)],
    "O": [(0, 0), (0, -1), (1, 0), (1, -1)],
    "J": [(0, 0), (-1, 0), (0, -1), (0, -2)],
    "L": [(0, 0), (1, 0), (0, -1), (0, -2)],
    "I": [(0, 0), (0, 1), (0, -1), (0, -2)],
    "S": [(0, 0), (1, 0), (0, -1), (-1, -1)],
    "Z": [(0, 0), (1, 0), (0, -1), (1, -1)],
}
