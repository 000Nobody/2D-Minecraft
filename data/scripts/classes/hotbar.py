import pygame
import os

from ...variables import *
from ..core_functions import draw_rect_alpha

imgs_dir = 'data/imgs/block_previews'

font = pygame.font.Font('data/fonts/minecraft_font.ttf', 23)

class Hotbar:

	def __init__(self):
		self.width = WINDOW_SIZE[0]//3
		self.height = self.width//9
		self.slot_width = self.width//9
		self.slot_height = self.slot_width
		self.x = WINDOW_SIZE[0]//2 - self.width//2
		self.y = WINDOW_SIZE[1] - WINDOW_SIZE[1]//7
		self.selected_slot = 1

		self.base_rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.slot_rects = {}
		x = self.x
		for i in range(9):
			rect = pygame.Rect(x, self.y, self.slot_width, self.slot_height)
			self.slot_rects[i+1] = rect
			x += self.slot_width

		self.slot_contents = {
				1: [],
				2: [],
				3: [],
				4: [],
				5: [],
				6: [],
				7: [],
				8: [],
				9: []
			}

		self.block_preview_imgs = {}
		for img in os.listdir(imgs_dir):
		    loaded_img = pygame.image.load(imgs_dir + '/' + img).convert_alpha()
		    loaded_img = pygame.transform.scale(loaded_img, (self.slot_width-10, self.slot_height-10))
		    img_name = img.split('.')[0]
		    self.block_preview_imgs[img_name] = loaded_img


	def get_available_slot(self, block_type):
		# First check if there is a slot which the item can be added with another item
		for i, n in self.slot_contents.items():
			if n != []:
				if n[0] == block_type and n[1] < STACK_SIZE:
					return i

		# If not, returns the first available slot
		for i, n in self.slot_contents.items():
			if n == []:
				return i


	def add_block_to_slot(self, block_type, amount):
		slot = self.get_available_slot(block_type)
		if self.slot_contents[slot] == []:
			self.slot_contents[slot] = [block_type, amount]
		else:
			self.slot_contents[slot][1] += amount


	def draw(self, display):
		draw_rect_alpha(display, (0, 0, 0, 50), self.base_rect)
		for index, rect in self.slot_rects.items():
			if index != self.selected_slot:
				pygame.draw.rect(display, (25, 25, 25), rect, 4)
		# Drawing selected slot after the rest so that it is drawn on top of other slots
		pygame.draw.rect(display, (200, 200, 200), self.slot_rects[self.selected_slot], 5)

		for i, n in self.slot_contents.items():
			if n != []:
				centering_rect = self.block_preview_imgs[n[0]].get_rect()
				centering_rect.center = self.slot_rects[i].center
				display.blit(self.block_preview_imgs[n[0]], centering_rect.topleft)

				if n[1] > 1:
					font_render = font.render(str(n[1]), True, (200, 200, 200))
					font_centering_rect = font_render.get_rect()
					font_centering_rect.bottomright = centering_rect.bottomright
					display.blit(font_render, font_centering_rect.topleft)


	def update(self):
		self.selected_slot_content = self.slot_contents[self.selected_slot]
		for i, n in self.slot_contents.items():
			if n != []:
				if n[1] <= 0:
					self.slot_contents[i] = []