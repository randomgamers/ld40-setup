import pygame
from typing import List, Tuple
from ..utils import load_image, load_image_norect
from .. import config


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

        self.walk_path = walk_path

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (30, 30)
        self.speed_x = 0
        self.speed_y = 0
        self.walking = False

    def update(self):
        # sprite update
        if self.walking :
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

    def _walk(self):
        newpos = self.rect.move((self.speed_x, self.speed_y))
        self.rect = newpos
