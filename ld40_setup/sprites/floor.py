import pygame
from .. import config
from .. import utils


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = utils.load_image('map/floor50.png')
        self.rect.move_ip(x * config.TILE_SIZE, y * config.TILE_SIZE)
