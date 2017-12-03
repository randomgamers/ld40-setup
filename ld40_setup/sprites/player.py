from collections import defaultdict

import pygame
import numpy as np
import random

from .. import config
from ..utils import load_image_norect
from ..game_sound import GameSound
from .animated_sprite import AnimatedSprite

class Player(AnimatedSprite):
    """Player sprite."""

    def __init__(self, position, walls):

        super().__init__(image_dir='characters/player/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position)

        # TODO: this shuld be somewhere else
        self.walls = walls
        self.busted = False
        self.dead = False
        self.dead_count = 0

        # collision rectangles
        self.collision_rect = self.rect.inflate(-self.rect.w*0.5, -self.rect.h*0.4)
        self.light_collision_rect = self.rect.inflate(-self.rect.w * 0.7, -self.rect.h * 0.25)

        # visualization of collider TODO: remove
        self.collision_sprite = pygame.sprite.Sprite()
        self.collision_sprite.rect = self.light_collision_rect
        self.collision_sprite.image = pygame.Surface((self.light_collision_rect.w, self.light_collision_rect.h))
        self.collision_sprite.image.fill((255, 125, 0))

        # train stuff
        self.train = []
        self.position_history = []
        self.hostage_init_delay = defaultdict(int)
        self.wait_position_history_delete = int(config.TRAIN_DELAY * 2 * config.FPS)

        # player stuff
        self.dizzy = 0
        self.walking = False
        self.flipped = False
        self.walking_speed = self.update_walking_speed()

        # idle state
        self.idle_image = load_image_norect('characters/player/idle.png', True)

        # allowed directions of move
        self.allowed_directions = dict(left=True, right=True, top=True, bottom=True)

        # number of saved hostages
        self.num_saved_hostages = 0

        # Busted sounds
        self.busted_sounds = ['character/ohshit.ogg', 'character/fuckfuckFUCK.ogg', 'character/notagainman.ogg', 'character/FUCK.ogg']

    def set_busted(self):
        if self.busted:
            return

        self.busted = True
        GameSound(self.busted_sounds[random.randrange(len(self.busted_sounds))]).play()

    def update_walking_speed(self):
        train_slowdown = 1.0
        if len(self.train) > 0:
            train_slowdown = np.max([hostage.slowdown for hostage in self.train])

        self.walking_speed = int(config.PLAYER_SPEED / config.FPS / train_slowdown)
        return self.walking_speed

    def collision_check(self, _, wall):
        return self.collision_rect.colliderect(wall.rect)

    def update(self):
        # sprite update
        self.collision_rect.center = (self.rect.center[0], self.rect.center[1] + 0.2*self.rect.h)
        self.light_collision_rect.center = (self.rect.center[0], self.rect.center[1] + 0.05 * self.rect.h)

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

        # update position history
        if self.speed_x != 0 or self.speed_y != 0:
            self.position_history.append(self.rect.center)

        # animate/idle based on speed
        if self.speed_x != 0 or self.speed_y != 0:
            self.animate()
        else:
            self.set_idle()

        # move train
        for i, hostage in enumerate(self.train):
            if self.hostage_init_delay[i] <= 0:
                hostage.move_to(self.position_history[int(-config.TRAIN_DELAY * (i+1) * config.FPS)])
                hostage.waiting = False
            elif self.speed_x != 0 or self.speed_y != 0:
                hostage.waiting = True
                self.hostage_init_delay[i] -= 1

        # prune position history
        if self.speed_x != 0 or self.speed_y != 0:
            min_history_len = int(config.TRAIN_DELAY * (len(self.train)+3) * config.FPS)
            if len(self.position_history) > min_history_len and self.wait_position_history_delete <= 0:
                self.position_history = self.position_history[-min_history_len:]
                self.wait_position_history_delete = min_history_len
            else:
                self.wait_position_history_delete -= 1

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
        self.hostage_init_delay[len(self.train)-1] = config.TRAIN_DELAY * (len(self.train)+1) * config.FPS
        self.update_walking_speed()
        hostage.play_track(hostage.add_sounds[random.randrange(len(hostage.add_sounds))])

    def remove_from_train(self, hostage):
        self.train.remove(hostage)
        hostage.soundwave.kill()
        self.num_saved_hostages += 1
        self.update_walking_speed()
