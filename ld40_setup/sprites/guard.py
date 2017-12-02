import pygame
import numpy as np
from typing import List, Tuple
from ..utils import load_image, load_image_norect
from .. import config


def tile_to_px(tile_x, tile_y):
    return tile_x*10, tile_y*10


def px_to_tile(px_x, px_y):
    return px_x//10, px_y//10


class Guard(pygame.sprite.Sprite):

    def __init__(self, walk_path: List[Tuple[int, int]]):
        super().__init__()

        self.images = []
        self.images.append(load_image_norect('runsprite/run001.png', -1))
        self.images.append(load_image_norect('runsprite/run002.png', -1))
        self.images.append(load_image_norect('runsprite/run003.png', -1))
        self.images.append(load_image_norect('runsprite/run004.png', -1))
        self.images.append(load_image_norect('runsprite/run005.png', -1))
        self.images.append(load_image_norect('runsprite/run006.png', -1))
        self.images.append(load_image_norect('runsprite/run007.png', -1))
        self.images.append(load_image_norect('runsprite/run008.png', -1))

        self.image, self.rect = load_image('runsprite/run001.png', -1)
        self.image_index = 0

        self.frame_wait_counter = 0
        self.frame_wait_max = config.FPS
        self.frame_wait_max /= len(self.images)
        self.frame_wait_max /= 3

        assert len(walk_path) > 1
        self.walk_path = walk_path
        self.path_progress = 0
        self.path_forward = True
        self.next_tile_to = self.walk_path[1]
        self.speed_x, self.speed_y = 0, 0

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = tile_to_px(*self.walk_path[0])

        self.update_speed()

    def next_path_part(self):
        if self.path_forward:
            if self.path_progress == len(self.walk_path) - 1:
                self.path_forward = False
                self.next_tile_to = self.walk_path[len(self.walk_path) - 2]
            else:
                self.next_tile_to = self.walk_path[self.path_progress + 1]
                self.path_progress += 1
        else:
            if self.path_progress == 0:
                self.path_forward = True
                self.next_tile_to = self.walk_path[1]
            else:
                self.next_tile_to = self.walk_path[self.path_progress - 1]
                self.path_progress -= 1

    def update_speed(self):
        tile_current = self.current_tile()
        # print(self.next_tile_to[0] - tile_current[0], self.next_tile_to[1] - tile_current[1])
        self.speed_x = np.sign(self.next_tile_to[0] - tile_current[0])
        self.speed_y = np.sign(self.next_tile_to[1] - tile_current[1])

    def current_tile(self):
        return px_to_tile(*self.rect.center)

    def update(self):

        # move
        self.rect.move_ip((self.speed_x, self.speed_y))

        # update path progress
        if self.next_tile_to == self.current_tile():
            self.next_path_part()
            self.update_speed()

        self.frame_wait_counter += 1
        if self.frame_wait_counter >= self.frame_wait_max:
            self.frame_wait_counter = 0
            self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0

        # flipping hoizontally
        if self.speed_x < 0:
            self.image = pygame.transform.flip(self.images[self.image_index], True, False)
        else :
            self.image = self.images[self.image_index]
