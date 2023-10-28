# Music.py

import pygame as pg

### Replace X with custom file path on your computer.###
def play_background_music():
    pg.mixer.init()
    pg.mixer.music.load('XTRACK22-1.wav')  # Replace with the path to your music file
    pg.mixer.music.play(-1)  # -1 means loop indefinitely
    pg.mixer.music.set_volume(0.5)  # This sets the volume to 50%

### Replace X with custom file path on your computer.###
def play_score_sound():
    score_sound = pg.mixer.Sound('Xcym.wav')  # Replace with the path to your score sound effect file
    score_sound.play(0)
    score_sound.set_volume(0.5)  # This sets the volume to 50%
    score_sound = pg.mixer.Sound(score_sound)




