import pygame
from .. import config
from .. import utils


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, type='D'):
        pygame.sprite.Sprite.__init__(self)

        if type == 'D':
            self.door_image = utils.load_image('map/door_bottom_50.png')
        elif type == 'G':
            self.door_image = utils.load_image('map/door_top_horizontal_50.png')
        elif type == 'F':
            self.door_image = utils.load_image('map/door_top_vertical_50.png')
        self.image, self.rect = self.door_image
        self.rect.move_ip(x * config.TILE_SIZE, y * config.TILE_SIZE)
