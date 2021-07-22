import pygame
import os

from ...variables import * 

pygame.init()
pygame.display.set_mode()

imgs_dir = 'data/imgs/blocks'

block_imgs = {}
for img in os.listdir(imgs_dir):
    loaded_img = pygame.image.load(imgs_dir + '/' + img).convert_alpha()
    loaded_img = pygame.transform.scale(loaded_img, (TILE_SIZE, TILE_SIZE))
    img_name = img.split('.')[0]
    block_imgs[img_name] = loaded_img

class Block:

	def __init__(self, chunk, pos, block_type):
		self.chunk = chunk
		self.pos = pos 
		self.type = block_type
		self.x = pos[0]
		self.y = pos[1]
		self.coords = (self.x//TILE_SIZE, self.y//TILE_SIZE)
		self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

	@property
	def img(self):
		img = block_imgs[self.type]
		return img


	def get_scrolled_rect(self, scroll):
		rect = pygame.Rect(self.x - scroll[0], self.y - scroll[1], TILE_SIZE, TILE_SIZE)
		return rect

	def get_scrolled_pos(self, scroll):
		pos = (self.x - scroll[0], self.y - scroll[1])
		return pos
		