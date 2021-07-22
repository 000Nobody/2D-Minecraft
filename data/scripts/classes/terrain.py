import pygame
import perlin
import random

from .block import Block
from ...variables import *

p = perlin.Perlin(random.randint(0, 10000))

class Terrain:

    def __init__(self):
        self.map = []
        self.tile_rects = []
        self.placed_blocks = []


    def generate_chunk(self, x, y):
        if (x, y) not in [block.chunk for block in self.map]:

            for y_pos in range(CHUNK_SIZE):
                for x_pos in range(CHUNK_SIZE):

                    block_added = False

                    target_x = x * CHUNK_SIZE + x_pos
                    target_y = y * CHUNK_SIZE + y_pos

                    height = p.one(target_x)

                    if target_y > CHUNK_SIZE + 3 - height:
                        tile_type = 'stone'
                    elif target_y > CHUNK_SIZE - height:
                        tile_type = 'dirt'
                    elif target_y == CHUNK_SIZE - height:
                        tile_type = 'grass'
                    else:
                        tile_type = 'air'

                    for block in self.placed_blocks:
                        if block.coords == (target_x, target_y):
                            self.map.append(block)
                            block_added = True

                    if not block_added:
                        self.map.append(Block((x, y), (target_x * TILE_SIZE, target_y * TILE_SIZE), tile_type))


    def unload_chunk(self, chunk_pos):
        for block in self.map:
            if block.chunk == chunk_pos:
                self.map.remove(block)


    def remove_block(self, block_pos):
        for i, block in enumerate(self.map):
            if block.pos == block_pos:
                self.map[i].type = 'air'
                self.placed_blocks.append(self.map[i])


    def add_block(self, block_pos, block_type):
        for i, block in enumerate(self.map):
            if block.pos == block_pos:
                if block.type == 'air':
                    self.map[i].type = block_type
                    self.placed_blocks.append(self.map[i])


    def generate_hitbox(self):
        self.tile_rects = []
        for block in self.map:
            if block.type != 'air':
                self.tile_rects.append(block.rect)


    def draw(self, display):
        for block in self.map:
            display.blit(block.img, block.get_scrolled_pos(scroll))

            # scrolled_rect = block.get_scrolled_rect(scroll)
            # if block.type == 'grass':
            #     pygame.draw.rect(display, 'green', scrolled_rect)
            # elif block.type == 'dirt':
            #     pygame.draw.rect(display, 'brown', scrolled_rect)
            # elif block.type == 'stone':
            #     pygame.draw.rect(display, 'dark grey', scrolled_rect)


    def update(self, player):
        self.generate_hitbox()
        for y in range(RENDER_DISTANCE):
            for x in range(RENDER_DISTANCE):
                target_x = x + player.current_chunk[0] - RENDER_DISTANCE//2
                target_y = y + player.current_chunk[1] - RENDER_DISTANCE//2
                self.generate_chunk(target_x, target_y)
