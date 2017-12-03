import pygame
from .. import config
from .. import utils


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, type='.'):
        pygame.sprite.Sprite.__init__(self)

        if type == '.':
            self.floor_image = utils.load_image('map/floor_50.png')
        elif type == ',':
            self.floor_image = utils.load_image('map/safe_floor_50.png')
        elif type == 'E':
            self.floor_image = utils.load_image('map/wall50.png')
        self.image, self.rect = self.floor_image
        self.rect.move_ip(x * config.TILE_SIZE, y * config.TILE_SIZE)
