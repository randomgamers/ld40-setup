import os, sys
import pygame
from pygame.locals import *
from . import config


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
