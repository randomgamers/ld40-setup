import pygame
import numpy as np

from .. import config
from ..utils import load_image, load_image_norect
from .animated_sprite import AnimatedSprite


class Player(AnimatedSprite):
    """Player sprite."""

    def __init__(self, walls):

        super().__init__(image_dir='characters/player/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=(10, 10))

        # TODO: this shuld be somewhere else
        self.walls = walls

        # collision rectangle
        self.collision_rect = self.rect.inflate(-self.rect.w*0.5, -self.rect.h*0.15)

        # visualization of collider TODO: remove
        self.collision_sprite = pygame.sprite.Sprite()
        self.collision_sprite.rect = self.collision_rect
        self.collision_sprite.image = pygame.Surface((self.collision_rect.w, self.collision_rect.h))
        self.collision_sprite.image.fill((255, 125, 0))

        # player stuff
        self.dizzy = 0
        self.walking = False
        self.flipped = False
        self.walking_speed = int(config.PLAYER_SPEED / config.FPS)

        # allowed directions of move
        self.allowed_directions = dict(left=True, right=True, top=True, bottom=True)

        # train stuff
        self.train = []
        self.position_history = []

    def collision_check(self, _, wall):
        return self.collision_rect.colliderect(wall.rect)

    def update(self):
        # sprite update
        self.collision_rect.center = self.rect.center

        for direction, _ in self.allowed_directions.items():
            self.allowed_directions[direction] = True

        collisions = pygame.sprite.spritecollide(self, self.walls, False, collided=self.collision_check)
        if collisions:
            for collision in collisions:
                x_offset = self.collision_rect.center[0] - collision.rect.center[0]
                y_offset = self.collision_rect.center[1] - collision.rect.center[1]
                x_offset_threshold = self.collision_rect.w / 2
                y_offset_threshold = self.collision_rect.h / 2
                if abs(x_offset) - config.TILE_SIZE/2 < x_offset_threshold and abs(y_offset) - config.TILE_SIZE/2 < y_offset_threshold*0.5:
                    direction = 'left' if x_offset > 0 else 'right'
                    self.allowed_directions[direction] = False
                if abs(y_offset) - config.TILE_SIZE/2 < y_offset_threshold and abs(x_offset) - config.TILE_SIZE/2 < x_offset_threshold*0.25:
                    direction = 'top' if y_offset > 0 else 'bottom'
                    self.allowed_directions[direction] = False

        # check that player doesnt go into a wall
        x_direction = 'left' if self.speed_x < 0 else 'right'
        y_direction = 'top' if self.speed_y < 0 else 'bottom'

        if not self.allowed_directions[x_direction]:
            self.speed_x = 0
        if not self.allowed_directions[y_direction]:
            self.speed_y = 0

        # almost like super update
        speed_x, speed_y = self.normalize_speed()
        self.rect.move_ip((speed_x, speed_y))

        if self.speed_x != 0 or self.speed_y != 0:
            self.position_history.append(self.rect.center)

        if self.speed_x != 0 or self.speed_y != 0 or (self.image_index != 2 and self.image_index != 6):
            self.animate()

        # move train
        for i, hostage in enumerate(self.train):
            hostage.move_to(self.position_history[-10 * (i+1)])
            # hostage.speed_x, hostage.speed_y = self.position_history[-10 * i]

    def normalize_speed(self):
        normalization_factor = np.sqrt(((self.speed_x/self.walking_speed)**2 + (self.speed_y/self.walking_speed)**2))
        if normalization_factor == 0:
            return 0, 0

        return self.speed_x / normalization_factor, self.speed_y / normalization_factor

    def move_x(self, speed):
        self.speed_x = self.walking_speed * np.sign(speed)

    def move_y(self, speed):
        self.speed_y = self.walking_speed * np.sign(speed)

    def stop_walk(self):
        self.speed_x = 0
        self.speed_y = 0

    def add_to_train(self, hostage):
        self.train.append(hostage)
        print('added to train')
