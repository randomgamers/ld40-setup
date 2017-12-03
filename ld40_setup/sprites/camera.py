import pygame
import math
from .rotating_sprite import RotatingSprite
from .light_particle import LightParticle
from .. import config


class Camera(RotatingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='',
                         image_file='camera_small.png',
                         **kwargs)

        self.particles = pygame.sprite.Group()
        self.particle_rect = pygame.Rect(0, 0, 600, 600)
        self.particle_rect.center = self.rect.center
        self.particle_sprite = pygame.sprite.Sprite()
        self.particle_sprite.rect = self.particle_rect
        self.particle_sprite.image = pygame.Surface((self.particle_rect.w, self.particle_rect.h))

        self.particle_origin = (0, 0)

        self.collision_rect = pygame.Rect(0, 0, 0, 0)
        self.collision_rect.center = self.rect.center

    def vyser_particle(self, particle_id):
        self.particles.add(LightParticle(particle_id, self))

    def update(self):
        self.direction = -self.angle_current

        light_offset_x = self.rect.center[0] + 25*math.cos(math.radians(self.direction - 45))
        light_offset_y = self.rect.center[1] + 25*math.sin(math.radians(self.direction - 45))
        self.particle_origin = (light_offset_x, light_offset_y)

        if len(self.particles) < config.LIGHT_PARTICLE_COUNT:
            for i in range(config.LIGHT_PARTICLE_BATCH_SIZE):
                self.vyser_particle(i)

        super().update()
