import pygame
import random

from ...variables import *
from ..core_functions import distance
from .block import Block

class Tree:

	def __init__(self, base_pos):
		self.base_pos = base_pos
		self.trunk_height = random.randint(2, 5)
		self.leaf_radius = 3
		self.blocks = []

		y = 0
		for i in range(self.trunk_height):
			block = Block((self.base_pos[0], self.base_pos[1] - y), 'wood')
			self.blocks.append(block)
			y += TILE_SIZE

		leaf_center_rect = self.blocks[-random.randint(1, 2)].rect
		leaf_domain = []
		for i in range(self.leaf_radius):
			for j in range(self.leaf_radius):
				x1 = leaf_center_rect.topleft[0] + (i * TILE_SIZE)
				x2 = leaf_center_rect.topleft[0] - (i * TILE_SIZE)
				y1 = leaf_center_rect.topleft[1] + (j * TILE_SIZE)
				y2 = leaf_center_rect.topleft[1] - (j * TILE_SIZE)
				leaf_domain.append((x1, y1))
				leaf_domain.append((x2, y2))
				leaf_domain.append((x2, y1))
				leaf_domain.append((x1, y2))


		for pos in leaf_domain:
			print(distance(pos, leaf_center_rect.center))
			if distance(pos, leaf_center_rect.center) <= (self.leaf_radius-1)*TILE_SIZE:
				self.blocks.append(Block(pos, 'leaf'))


				

		



