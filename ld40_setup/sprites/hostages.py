from typing import Tuple
import pygame
import random

from .. import config
from ..utils import load_image_norect, load_image, game_pixel_to_coord
from ..sound import GameSound

from .animated_sprite import AnimatedSprite


class Soundwave(AnimatedSprite):
    def __init__(self, parent, radius):
        super().__init__(image_dir='soundwaves/circles/{}'.format(radius*2),
                         image_files=['circle_0{}.png'.format(str(i).zfill(2)) for i in range(1, 13)],
                         position=(0, 0), skip_frames=True)
        self.parent = parent
        self.image, self.rect = load_image('soundwaves/circle.png', use_alpha=True)
        self.radius = radius
        self.enabled = False

    def update(self):
        super().update()

        if self.enabled:
            self.rect.center = (self.parent.rect.center[0] + self.parent.rect.w / 2 - self.radius, self.parent.rect.center[1] + self.parent.rect.h / 2 - self.radius)
        else:
            self.rect.center = (-1000, -1000)
        # # self.image = pygame.transform.scale(self.original_image, (self.radius * 2, self.radius * 2))
        # alpha = int(120 * (1 - (self.radius / max(self.radius, self.soundwave_radius))))
        # # print(alpha)
        # # self.image.set_alpha(128)
        # # self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        #
        # if self.radius > self.soundwave_radius:
        #     self.reset()


class Hostage(AnimatedSprite):
    def __init__(self, image_dir, image_files, position, player, entry_tile, end_tiles, soundwave_radius, sounds):
        super().__init__(image_dir=image_dir, image_files=image_files, position=position)

        # general stats
        self.noise = 0
        self.slowdown = 1.0

        # train stuff
        self.player = player
        self.in_train = False

        # collision rectangle
        self.collision_rect = self.rect.inflate(-self.rect.w*0.5, -self.rect.h*0.15)

        # visualization of collider TODO: remove
        # self.collision_sprite = pygame.sprite.Sprite()
        # self.collision_sprite.rect = self.collision_rect
        # self.collision_sprite.image = pygame.Surface((self.collision_rect.w, self.collision_rect.h))
        # self.collision_sprite.image.fill((255, 125, 0))

        # last speeds
        self.last_position = position

        # waiting for adding to train
        self.waiting = False

        # entry tile
        self.entry_tile = entry_tile

        # end tiles
        self.end_tiles = end_tiles

        # soundwaves
        self.soundwave_radius = soundwave_radius
        self.soundwave = Soundwave(self, soundwave_radius)

        self.light_collision_rect = self.rect.inflate(-self.rect.w * 0.7, -self.rect.h * 0.25)

        # Sounds
        self.sounds = sounds
        self.soundwave_timer = 0
        self.reset_sound()

    def reset_sound(self):
        self.next_sound_at = random.randrange(config.MIN_PLAY_SOUND_AT * config.FPS, config.MAX_PLAY_SOUND_AT * config.FPS)

    def collision_check(self, _, player):
        return self.collision_rect.colliderect(player.rect)

    def play_sound(self):
        GameSound(self.sounds[random.randrange(len(self.sounds))]).play()
        self.soundwave.enabled = True
        self.soundwave_timer = config.MAX_SOUNDWAVE_TIMER * config.FPS

    def update(self):
        # compute deltas
        dx = self.rect.centerx - self.last_position[0]
        dy = self.rect.centery - self.last_position[1]

        # update last position
        self.last_position = self.rect.center

        if dx != 0 or dy != 0:  # instead of super update
            self.animate()

        elif dx == 0 and dy == 0:
            if self.waiting:
                self.flipped = not self.flipped
            self.set_idle()

        if dx > 0:
            self.flipped = True
        elif dx < 0:
            self.flipped = False

        self.collision_rect.center = self.rect.center
        self.light_collision_rect.center = (self.rect.center[0], self.rect.center[1] + 0.05 * self.rect.h)

        collisions = pygame.sprite.spritecollide(self, [self.player], False, collided=self.collision_check)
        if collisions:
            for collision in collisions:
                if not self.in_train:
                    self.player.add_to_train(self)
                    self.in_train = True

        for end_coord in self.end_tiles + [self.entry_tile]:
            if game_pixel_to_coord(self.rect.center) == end_coord:
                self.player.remove_from_train(self)
                self.kill()

        # sounds
        self.next_sound_at -= 1
        if self.next_sound_at <= 0:
            self.reset_sound()
            self.play_sound()

        if self.soundwave_timer <= 0:
            self.soundwave.enabled = False
        else:
            self.soundwave_timer -= 1


    def move_to(self, new_position: Tuple[int,int]):
        self.rect.center = self.collision_rect.center = new_position


class NoisyChick(Hostage):
    def __init__(self, position, player, entry_tile, end_tiles):
        super().__init__(image_dir='characters/hostage1/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position,
                         player=player,
                         entry_tile=entry_tile,
                         end_tiles=end_tiles,
                         soundwave_radius=100,
                         sounds=['punch.wav', 'whiff.wav'])
        self.noise = 1
        self.idle_image = load_image_norect('characters/hostage1/idle.png', True)


class FatGuy(Hostage):
    def __init__(self, position, player, entry_tile, end_tiles):
        super().__init__(image_dir='characters/hostage2/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position,
                         player=player,
                         entry_tile=entry_tile,
                         end_tiles=end_tiles,
                         soundwave_radius=100,
                         sounds=['punch.wav', 'whiff.wav'])
        self.slowdown = 2

        self.idle_image = load_image_norect('characters/hostage2/idle.png', True)


class RegularGuy(Hostage):
    def __init__(self, position, player, entry_tile, end_tiles):
        super().__init__(image_dir='characters/hostage3/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position,
                         player=player,
                         entry_tile=entry_tile,
                         end_tiles=end_tiles,
                         soundwave_radius=25,
                         sounds=['punch.wav', 'whiff.wav'])

        self.idle_image = load_image_norect('characters/hostage3/idle.png', True)


