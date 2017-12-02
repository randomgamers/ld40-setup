import pygame
from .wandering_sprite import WanderingSprite
from .light_particle import LightParticle
from .. import config


class Guard(WanderingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='characters/guard/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         **kwargs)

        self.particles = pygame.sprite.Group()
        self.direction = 0
        self.last_position = [0, 0]

    def vyser_particle(self, particle_id):
        self.particles.add(LightParticle(particle_id, self))

    def update(self):
        super().update()

        # compute deltas
        dx = self.rect.centerx - self.last_position[0]
        dy = self.rect.centery - self.last_position[1]

        if dx > 0:
            self.direction = 0
        elif dx < 0:
            self.direction = 180
        elif dy > 0:
            self.direction = 90
        elif dy < 0:
            self.direction = 270

        # update last position
        self.last_position = self.rect.center

        if len(self.particles) < config.LIGHT_PARTICLE_COUNT:
            for i in range(config.LIGHT_PARTICLE_BATCH_SIZE):
                self.vyser_particle(i)
