import os, sys
import pygame
from . import config
import math


class LoadError(RuntimeError):
    pass


def load_image(image_name, use_alpha=False):
    fullname = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.IMAGES_DIR, image_name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as ex:
        raise LoadError('Cannot load `{}`'.format(image_name)) from ex
    if use_alpha :
        image = image.convert_alpha()
    else :
        image = image.convert()
    return image, image.get_rect()


def load_image_norect(image_name, use_alpha=False):
    image, rect = load_image(image_name, use_alpha)
    return image


class NoneSound:
    def play(self): pass


def load_sound(sound_name):
    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.SOUNDS_DIR, sound_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as ex:
        raise LoadError('Cannot load `{}`'.format(sound_name)) from ex
    return sound


def coord_to_game_pixel(coord):
    x, y = coord
    return x * config.TILE_SIZE, y * config.TILE_SIZE


def game_pixel_to_coord(game_pixel):
    x, y = game_pixel
    return x // config.TILE_SIZE, y // config.TILE_SIZE


def dist(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


fullscreen = False


def init_screen(fullscreen):
    flags = pygame.FULLSCREEN|pygame.DOUBLEBUF if fullscreen else 0

    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
        true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        return pygame.display.set_mode(true_res, flags)
    else:
        return pygame.display.set_mode((0, 0), flags)


def toggle_fullscreen(screen):
    global fullscreen
    
    if pygame.display.get_driver() == 'x11':
        pygame.display.toggle_fullscreen()
    else:
        screen_copy = screen.copy()
        if fullscreen:
            screen = init_screen(False)
        else:
            screen = init_screen(True)
            screen.blit(screen_copy, (0, 0))
            pygame.display.update()
        fullscreen = not fullscreen
    return screen