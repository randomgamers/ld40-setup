import os
from typing import List, Tuple

import pygame

from ..utils import load_image, load_image_norect
from .. import config


def tile_to_px(tile_x, tile_y):
    """TODO: need @gyfis's update"""
    return tile_x*10, tile_y*10


def px_to_tile(px_x, px_y):
    """TODO: need @gyfis's update"""
    return px_x//10, px_y//10


class AnimatedSprite(pygame.sprite.Sprite):
    """Basic animated and moveable sprite."""

    def __init__(self, image_dir: str, image_files: List[str], position: Tuple[int, int], speed: Tuple[int, int]=(0,0)):
        super().__init__()
        assert len(image_files) > 0, 'Animated sprite must contain at least one image.'

        # load images
        self.images = [load_image_norect(os.path.join(image_dir, image_file), True)
                       for image_file in image_files]

        # set up current image
        self.image, self.rect = load_image(os.path.join(image_dir, image_files[0]), True)
        self.image_index = 0

        # frames-realted stuff
        self.frame_wait_counter = 0
        self.frame_wait_max = config.FPS
        self.frame_wait_max /= len(self.images)
        self.frame_wait_max /= 3

        # init. position
        self.rect.center = tile_to_px(*position)

        # Save the last direction the character was facing
        self.flipped = False

        # save speed
        self.speed_x, self.speed_y = speed

    def update(self):
        """Move the sprite and animate it."""
        super().update()
        self.rect.move_ip((self.speed_x, self.speed_y))
        self.animate()

    def animate(self):
        """Change sprite image."""
        self.frame_wait_counter += 1
        if self.frame_wait_counter >= self.frame_wait_max:
            self.frame_wait_counter = 0
            self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0

        # flipping hoizontally
        if self.speed_x > 0 or (self.speed_x == 0 and self.flipped):
            self.image = pygame.transform.flip(self.images[self.image_index], True, False)
            self.flipped = True
        elif self.speed_x < 0 or (self.speed_x == 0 and not self.flipped):
            self.image = self.images[self.image_index]
            self.flipped = False

    @property
    def current_tile(self):
        return px_to_tile(*self.rect.center)
