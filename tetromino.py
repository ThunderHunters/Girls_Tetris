# tetromino

# Import necessary modules and classes
from Settings import *
import random

# Define the Block class for individual tetromino blocks
class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        # Initialize Block with tetromino and position
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        # Call the constructor of the parent class (Sprite)
        super().__init__(tetromino.tetris.sprite_group)
        # Set the image of the block to the tetromino's image
        self.image = tetromino.image

        self.rect = self.image.get_rect()

        # Set up special effects attributes
        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    # Check if the special effects animation should end
    def sfx_end_time(self):
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    # Run the special effects animation
    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    # Check if the block is alive and kill it if not
    def is_alive(self):
        if not self.alive:
            self.kill()

    # Rotate the block around a pivot position
    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    # Set the rectangle position of the block
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = (pos.x * TILE_SIZE, pos.y * TILE_SIZE)

    # Update the block's state
    def update(self):
        self.is_alive()
        self.set_rect_pos()

    # Check if the block collides with a position
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

# Define the Tetromino class for handling tetromino shapes
class Tetromino:
    def __init__(self, tetris, current=True):
       
        # Initialize Tetromino with the tetris game
        self.tetris = tetris
        # Choose a random shape for the tetromino
        self.shape = random.choice(list(TETROMINOS.keys()))
        # Choose a random image for the tetromino
        self.image = random.choice(tetris.app.images)
        # Create blocks based on the chosen shape
        self.blocks = [Block(self, pos) for pos in TETROMINOS[self.shape]]
        # Flag indicating if the tetromino is landing
        self.landing = False
        self.current = current

        self.next_pos_offset = NEXT_POS_OFFSET



    # Rotate the tetromino
    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    # Check if the tetromino collides with a set of block positions
    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    # Move the tetromino
    def move(self, direction, speed_multiplier=1):
            move_direction = MOVE_DIRECTIONS[direction]
            new_block_positions = [block.pos + move_direction for block in self.blocks]
            is_collide = self.is_collide(new_block_positions)

            if not is_collide:
                for block in self.blocks:
                    block.pos += move_direction * speed_multiplier
            elif direction == 'down':
                self.landing = True

    def update(self):
        # Adjust the positions of the blocks based on the new TILE_SIZE
        for block in self.blocks:
            block.set_rect_pos()

        self.move(direction='down')
