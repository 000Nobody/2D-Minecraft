import pygame
from os import listdir
from sys import exit

from data.scripts.classes.player import Player
from data.scripts.classes.terrain import Terrain
from data.scripts.classes.hotbar import Hotbar

from data.scripts.core_functions import draw, distance

from data.variables import *

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOW_SIZE)

player = Player((0, -200), TILE_SIZE-10, TILE_SIZE*2-10, 9, 13)
hotbar = Hotbar()
terrain = Terrain()
terrain.generate_chunk(0, 0)

while __name__ == '__main__':

    clock.tick(60)
    pygame.display.set_caption(str(int(clock.get_fps())))

    mx, my = pygame.mouse.get_pos()

    scroll[0] += int(
        (player.rect.x - scroll[0] - (WINDOW_SIZE[0]/2 + player.width/2 - 50)) / SCROLL_STIFF
    )
    scroll[1] += int(
        (player.rect.y - scroll[1] - (WINDOW_SIZE[1]/2 + player.height/2 - 100)) / SCROLL_STIFF
    )

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                player.jumping = True

            try:
                if int(pygame.key.name(event.key)) != 0:
                    hotbar.selected_slot = int(pygame.key.name(event.key))
            except ValueError:
                pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_a:
                player.moving_left = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                player.break_block(terrain, hotbar)
            if event.button == 3:
                player.place_block(terrain, hotbar)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if hotbar.selected_slot != 9:
                    hotbar.selected_slot += 1
                else:
                    hotbar.selected_slot = 1

            if event.button == 5:
                if hotbar.selected_slot != 1:
                    hotbar.selected_slot -= 1
                else:
                    hotbar.selected_slot = 9

    for chunk in list(set([i.chunk for i in terrain.map])):
        if distance(player.current_chunk, chunk) >= RENDER_DISTANCE:
            terrain.unload_chunk(chunk)

    player.get_selected_block(terrain, mx, my)

    terrain.update(player)
    player.update(terrain)
    hotbar.update()

    draw(screen, terrain, player, hotbar)

