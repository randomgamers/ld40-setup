import os, sys
import pygame
from pygame.locals import *
from . import config


class LoadError(RuntimeError):
    pass


def load_image(image_name, colorkey=None):
    fullname = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.IMAGES_DIR, image_name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as ex:
        raise LoadError from ex
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class NoneSound:
    def play(self): pass


def load_sound(sound_name):
    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.SOUNDS_DIR, sound_name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as ex:
        raise LoadError from ex
    return sound
