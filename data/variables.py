import pygame

WINDOW_SIZE = (1920, 1080) # Measured in pixels
GRAVITY_STRENGTH = 1
CHUNK_SIZE = 8 # Measured in blocks. I do not recommend changing this
TILE_SIZE = 64 # Measured in pixels
SCROLL_STIFF = 8 # How closely the camera follows the player (higher number = less stiff)
RENDER_DISTANCE = 5 # Measured in chunks
STACK_SIZE = 64 # Max number of blocks held in an inventory slot

scroll = [0, 0]