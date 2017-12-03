import pygame
from .rotating_sprite import RotatingSprite
from .light_particle import LightParticle
from .. import config


class Camera(RotatingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='',
                         image_file='camera_small.png',
                         **kwargs)

        self.particles = pygame.sprite.Group()
        self.particle_rect = pygame.Rect(0, 0, 30, 30)
        self.particle_rect.center = self.rect.center
        self.particle_sprite = pygame.sprite.Sprite()
        self.particle_sprite.rect = self.particle_rect
        self.particle_sprite.image = pygame.Surface((self.particle_rect.w, self.particle_rect.h))

        self.collision_rect = pygame.Rect(0, 0, 30, 30)
        self.collision_rect.center = self.rect.center

    def vyser_particle(self, particle_id):
        self.particles.add(LightParticle(particle_id, self))

    def update(self):
        self.direction = -self.angle_current
        if len(self.particles) < config.LIGHT_PARTICLE_COUNT:
            for i in range(config.LIGHT_PARTICLE_BATCH_SIZE):
                self.vyser_particle(i)

        super().update()
