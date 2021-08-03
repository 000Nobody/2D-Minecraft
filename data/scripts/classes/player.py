import pygame
import os

from ..core_functions import move, distance
from ...variables import *

class Player:

    def __init__(self, start_pos, width, height, vel, jump_height, reach_distance=4):

        self.width = width
        self.height = height
        self.vel = vel
        self.jump_height = jump_height
        self.reach_distance = reach_distance

        self.rect = pygame.Rect(start_pos[0], start_pos[1], width, height)
        self.coords = (self.rect.x//TILE_SIZE, self.rect.y//TILE_SIZE)
        self.pixel_coords = (self.coords[0] * TILE_SIZE, self.coords[1] * TILE_SIZE)

        self.jumping = False
        self.moving_right = False
        self.moving_left = False
        self.movement = [0, 0]
        self.selected_block = None
        self.current_chunk = (0, 0)
        self.inventory = []

        self.current_animation = 'idle'
        self.animations = self.load_animations('data/imgs/player')
        self.animation_counter = 0
        self.animation_flip = False


    def move(self, tile_rects):
        
        self.rect, self.collision_types, self.hit_list = move(self.rect, tile_rects, self.movement)

        if self.collision_types['bottom'] and not self.jumping:
            self.movement[1] = 1
        
        if not self.collision_types['bottom']:
            self.jumping = False
            self.movement[1] += GRAVITY_STRENGTH

        if self.collision_types['top']:
            self.movement[1] = 1

        if self.moving_right:
            self.movement[0] = self.vel
            self.current_animation = 'walk'
            self.animation_flip = False
        if self.moving_left:
            self.movement[0] = -self.vel
            self.current_animation = 'walk'
            self.animation_flip = True
        if self.jumping and self.collision_types['bottom']:
            self.movement[1] = -self.jump_height
            self.jumping = False

        if not self.moving_left and not self.moving_right:
            self.movement[0] = 0
            self.current_animation = 'idle'

        if self.movement[1] > 30:
             self.movement[1] = 30


    def get_selected_block(self, terrain, mx, my):
        mx += scroll[0]
        my += scroll[1]
        selected_coords = (mx//TILE_SIZE, my//TILE_SIZE)

        for block in terrain.map:
            if selected_coords == block.coords:
                if distance(selected_coords, self.coords) <= self.reach_distance:
                    if not block.rect.colliderect(self.rect):
                        self.selected_block = block
                    else:
                        self.selected_block = None
                else:
                    self.selected_block = None
                            

    def break_block(self, terrain, hotbar):
        self.current_animation = 'break'
        if self.selected_block and self.selected_block.type != 'air':
            self.inventory.append(self.selected_block.type)
            hotbar.add_block_to_slot(self.selected_block.type, 1)
            terrain.remove_block(self.selected_block.pos)


    def place_block(self, terrain, hotbar):
        self.current_animation = 'place'
        if (self.selected_block and self.selected_block.type == 'air'):
            if hotbar.selected_slot_content != []:
                if hotbar.selected_slot_content[1] > 0:
                    if terrain.add_block(self.selected_block.pos, hotbar.selected_slot_content[0]):
                        hotbar.slot_contents[hotbar.selected_slot][1] -= 1


    def load_animations(self, dir):
        animation_dict = {}
        for animation in os.listdir(dir):
            frame_list = []
            for frame in os.listdir(dir + '/' + animation):
                img = pygame.image.load(dir+'/'+animation+'/'+frame).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE*2-10, TILE_SIZE*2-10))
                frame_list.append(img)
            animation_dict[animation] = frame_list

        return animation_dict


    def draw(self, display):
        # temp_rect = pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.width, self.height)
        # pygame.draw.rect(display, 'white', temp_rect)

        if self.animation_counter//7 < len(self.animations[self.current_animation]):
            current_img = self.animations[self.current_animation][self.animation_counter//7]
        else:
            self.animation_counter = 0
            current_img = self.animations[self.current_animation][self.animation_counter//7]
        self.animation_counter += 1

        if self.animation_flip:
            current_img = pygame.transform.flip(current_img, True, False)

        scrolled_pos = (self.rect.x - scroll[0]-30, self.rect.y - scroll[1]+3)
        display.blit(current_img, scrolled_pos)

        if self.selected_block:
            block_rect = pygame.Rect(
                self.selected_block.x - scroll[0],
                self.selected_block.y - scroll[1],
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(display, 'black', block_rect, 3)


    def update(self, terrain):
        self.move(terrain.tile_rects)
        self.coords = (self.rect.x//TILE_SIZE, self.rect.y//TILE_SIZE)
        self.pixel_coords = (self.coords[0] * TILE_SIZE, self.coords[1] * TILE_SIZE)

        for block in terrain.map:
            if self.coords == block.coords:
                self.current_chunk = block.chunk
