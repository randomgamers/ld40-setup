import pygame
from pygame.locals import *
import math

from . import config
from .level import Level
from .utils import load_image


class Camera(object):
    def __init__(self, game_size, window_size):
        self.game_size = game_size
        self.window_size = window_size
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.wanted_position = [0, 0]

    def update(self):
        pos_diff = [float(self.wanted_position[i] - self.position[i]) for i in (0, 1)]
        distance = float(math.sqrt(pos_diff[0] ** 2 + pos_diff[1] ** 2))

        current_velocity = float(config.CAMERA_VELOCITY * distance / config.MAX_CAMERA_DISTANCE)
        for ax in (0, 1):
            self.velocity[ax] = current_velocity * pos_diff[ax] / distance
            self.position[ax] = self.position[ax] + self.velocity[ax]

    @property
    def blit_position(self):
        p = [(self.position[i] / self.game_size[i]) * self.window_size[i] for i in [0, 1]]
        return -self.position[0] + p[0], -self.position[1] + p[1]


class Scene(object):
    def __init__(self):
        self.level = Level(1)


def coord_to_game_pixel(coord, tile_size):
    return coord[1] * tile_size[0], coord[0] * tile_size[1]


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
    window_size = (2000, 1000)
    window.blit(game_screen, pygame.Rect(*camera.blit_position, *window_size))


def main():
    pygame.init()

    # User Screen
    screen = pygame.display.set_mode((0, 0))  # , pygame.FULLSCREEN)
    screen_size = screen.get_size()

    # Game screen
    game_size = (6500, 1500)
    game_screen = pygame.Surface(game_size)
    background = pygame.Surface(game_size)
    background = background.convert()

    # Viewing Window
    window_size = (2000, 1000)
    window = pygame.Surface(window_size)

    scene = Scene()
    camera = Camera(game_size, window_size)

    # g2sratio = game_size[0] / screen_size[0], game_size[1] / screen_size[1]

    # Tiles
    tiles = config.TILES
    tile_size = (window_size[0] / tiles[0], window_size[1] / tiles[1])

    tile, tile_rect = load_image('ball.png')

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
            game_screen.blit(tile, coord_to_game_pixel(coord, tile_size))

        camera.update()
        blit_game_to_window(game_screen, window, camera)
        scale_window_to_screen(window, screen)
        pygame.display.flip()
        # pygame.time.delay(15)


if __name__ == '__main__':
    main()
