import os
from typing import Tuple

import pygame

from ..utils import load_image, coord_to_game_pixel
from .. import config


def rotate_by_center___kindof(image, angle):
    """Rotate the given image... but not really."""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image, rot_rect


class RotatingSprite(pygame.sprite.Sprite):
    """Sprite rotating between given angles."""

    def __init__(self, angle_from: int, angle_to: int, rotation_speed: float, delay: float, image_dir: str,
                 image_file: str, position: Tuple[int, int]):
        """

        :param angle_from: degrees
        :param angle_to: degrees
        :param rotation_speed: degrees/second
        :param delay: second
        """
        super().__init__()

        assert angle_from < angle_to

        # load image
        self.image, self.rect = load_image(os.path.join(image_dir, image_file), -1)
        self.original = self.image

        # rotation setting
        self.angle_from = self.angle_current = angle_from
        self.angle_to = angle_to
        self.rotation_speed = int(rotation_speed / config.FPS)
        self.counterclockwise = True
        self.delay = delay

        # move image
        self.rect.center = coord_to_game_pixel(position)
        self.image = pygame.transform.rotate(self.image, self.angle_from)

        # delay counter
        self.frame_wait_counter = 0
        self.frame_wait_max = int(config.FPS / delay)
        self.edge_position = False

    def update(self):
        super().update()

        if self.edge_position:
            self.frame_wait_counter += 1
            if self.frame_wait_counter >= self.frame_wait_max:
                self.edge_position = False
                self.frame_wait_counter = 0
            return

        self.angle_current += self.rotation_speed * (1 if self.counterclockwise else -1)
        if self.angle_current > self.angle_to:
            self.counterclockwise = False
            self.angle_current = self.angle_to
            self.edge_position = True
        if self.angle_current < self.angle_from:
            self.counterclockwise = True
            self.angle_current = self.angle_from
            self.edge_position = True

        center_before = self.rect.center
        self.image, self.rect = rotate_by_center___kindof(self.original, self.angle_current)
        self.rect.center = center_before
