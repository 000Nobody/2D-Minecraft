import pygame
import perlin
from random import randint

from .block import Block
from .tree import Tree
from ...variables import *

p = perlin.Perlin(randint(0, 99999))

class Terrain:

    def __init__(self):
        self.map = []
        self.tile_rects = []
        self.placed_blocks = []
        self.loaded_chunks = []


    def generate_chunk(self, x, y):
        if (x, y) not in [block.chunk for block in self.map]:
            tree_blocks = []
            chunk_loaded = (x, y) in self.loaded_chunks

            for y_pos in range(CHUNK_SIZE):
                for x_pos in range(CHUNK_SIZE):

                    target_x = x * CHUNK_SIZE + x_pos
                    target_y = y * CHUNK_SIZE + y_pos

                    height = p.one(target_x)

                    if target_y == CHUNK_SIZE - 1 - height and randint(0, 6) == 0:
                        tree = Tree((target_x * TILE_SIZE, target_y * TILE_SIZE))
                        for tree_block in tree.blocks:
                            if tree_block.pos not in [i.pos for i in tree_blocks]:
                                tree_blocks.append(tree_block)

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
                        tile_type = 'grass_block'
                    elif target_y == CHUNK_SIZE - 1 - height and randint(0, 6) == 0 and not chunk_loaded:
                        tile_type = 'flower'
                    elif target_y == CHUNK_SIZE - 1 - height and randint(0, 3) == 0 and not chunk_loaded:
                        tile_type = 'grass'
                    else:
                        tile_type = 'air'

                    for block in self.placed_blocks:
                        if block.coords == (target_x, target_y):
                            self.map.append(block)
                            block_added = True

                    if not block_added:
                        if (target_x * TILE_SIZE, target_y * TILE_SIZE) in [i.pos for i in tree_blocks]:
                            if not chunk_loaded:
                                for tree_block in tree_blocks:
                                    if tree_block.pos == (target_x * TILE_SIZE, target_y * TILE_SIZE):
                                        self.map.append(tree_block)
                                        self.placed_blocks.append(tree_block)
                        else:
                            self.map.append(Block((target_x * TILE_SIZE, target_y * TILE_SIZE), tile_type))
                            if tile_type in ['flower', 'grass']:
                                self.placed_blocks.append(Block((target_x * TILE_SIZE, target_y * TILE_SIZE), tile_type))


            if not chunk_loaded:
                self.loaded_chunks.append((x, y))


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
                if block_type not in ['flower', 'grass']:
                    if block.type == 'air':
                        self.map[i].type = block_type
                        self.placed_blocks.append(self.map[i])
                        return True
                else:
                    for block2 in self.map:
                        if block2.pos == (block_pos[0], block_pos[1] + TILE_SIZE):
                            if block2.type != 'air':
                                self.map[i].type = block_type
                                self.placed_blocks.append(self.map[i])
                                return True
                            else:
                                return False


    def generate_hitbox(self):
        self.tile_rects = []
        for block in self.map:
            if block.type not in ['air', 'grass', 'flower']:
                self.tile_rects.append(block.rect)


    def draw(self, display):
        for block in self.map:
            display.blit(block.img, block.get_scrolled_pos(scroll))


    def update(self, player):
        self.generate_hitbox()
        for y in range(RENDER_DISTANCE):
            for x in range(RENDER_DISTANCE):
                target_x = x + player.current_chunk[0] - RENDER_DISTANCE//2
                target_y = y + player.current_chunk[1] - RENDER_DISTANCE//2
                self.generate_chunk(target_x, target_y)

        for i, block in enumerate(self.map):
            if block.type in ['flower', 'grass']:
                for block2 in self.map:
                    if block2.pos == (block.pos[0], block.pos[1] + TILE_SIZE):
                        if block2.type == 'air':
                            try:
                                self.placed_blocks.remove(self.map[i])
                            except ValueError:
                                pass
                            self.map[i].type = 'air'
