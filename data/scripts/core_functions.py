from data.variables import *
import pygame
import math

def draw(display, *classes):
    display.fill((227, 247, 255))

    for item in classes:
        if isinstance(item, list):
            for i in item:
                i.draw(display)

        else:
            item.draw(display)

    pygame.display.update()

def move(rect, tiles, movement):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_check(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_check(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types, hit_list


def collision_check(rect, tiles):
    hit_list = []
    for tile in tiles:
        if tile not in hit_list:
            if rect.colliderect(tile):
                hit_list.append(tile)
    return hit_list


def distance(pos1, pos2):
    x = (pos2[0] - pos1[0])**2
    y = (pos2[1] - pos1[1])**2
    return math.sqrt(x + y)


def draw_rect_alpha(display, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    display.blit(shape_surf, rect)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_death_screen(screen):
    WIDTH = WINDOW_SIZE[0]
    HEIGHT = WINDOW_SIZE[1]
    draw_text(screen, "You Died!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "You Fell From High Place", 40,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Noob", 30, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
