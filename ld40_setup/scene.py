import pygame
from pygame.locals import *
import math

from . import config
from .level import Level
from .utils import load_image

from .game_camera import GameCamera


class Scene(object):
    def __init__(self):
        self.level = Level(1)


def coord_to_game_pixel(coord):
    return coord[0] * config.TILE_SIZE, coord[1] * config.TILE_SIZE


def convert_coord(coord, ratio):
    return coord[0] * ratio[0], coord[1] * ratio[1]


def tadd(*tuples):
    total = [0 for _ in range(len(tuples[0]))]
    for t in tuples:
        for idx, i in enumerate(t):
            total[idx] += i
    return tuple(total)


def scale_window_to_screen(window, screen):
    pygame.transform.scale(window, screen.get_size(), screen)


def blit_game_to_window(game_screen, window, camera):
    window.blit(game_screen, pygame.Rect(*camera.blit_position, *window.get_size()))


def main():
    pygame.init()

    # User Screen
    screen = pygame.display.set_mode((0, 0))  # , pygame.FULLSCREEN)
    screen_size = screen.get_size()

    # Scene
    scene = Scene()

    # Game screen
    game_size = list(map(lambda shape: (shape + 5) * 100, scene.level.map_shape))
    game_screen = pygame.Surface(game_size)
    background = pygame.Surface(game_size)
    background = background.convert()

    # Tiles
    tiles = config.TILES

    # Viewing Window
    window_size = tiles[0] * config.TILE_SIZE, tiles[1] * config.TILE_SIZE
    window = pygame.Surface(window_size)

    camera = GameCamera(game_size, window_size)

    # g2sratio = game_size[0] / screen_size[0], game_size[1] / screen_size[1]

    tile, tile_rect = load_image('map/wall.png')

    clock = pygame.time.Clock()
    going = True
    # pygame.key.set_repeat(1, int(1000 / config.FPS))
    # pygame.display.flip()

    while going:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                s_mousepos = event.pos
                s_mousepos_perc = s_mousepos[0] / screen_size[0], s_mousepos[1] / screen_size[1]
                camera.wanted_position = [game_size[0] * s_mousepos_perc[0], game_size[1] * s_mousepos_perc[1]]

            # if event.type == KEYDOWN and event.key == K_LEFT:
            #     camera.acc[0] += 3
            # elif event.type == KEYDOWN and event.key == K_RIGHT:
            #     camera.acc[0] -= 3
            # elif event.type == KEYDOWN and event.key == K_UP:
            #     camera.acc[1] += 3
            # elif event.type == KEYDOWN and event.key == K_DOWN:
            #     camera.acc[1] -= 3

        game_screen.blit(background, (0, 0))
        for coord in scene.level.wall_coords:
            game_screen.blit(tile, coord_to_game_pixel(coord))

        camera.update()
        blit_game_to_window(game_screen, window, camera)
        scale_window_to_screen(window, screen)
        pygame.display.flip()
        # pygame.time.delay(15)


if __name__ == '__main__':
    main()
