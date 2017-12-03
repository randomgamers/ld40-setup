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
        self.removed_particles = pygame.sprite.Group()
        self.direction = 0
        self.last_position = [0, 0]

        self.particle_origin = (0, 0)

        # particle collision rectangle
        self.particle_rect = pygame.Rect(0, 0, 250, 60)
        self.particle_sprite = pygame.sprite.Sprite()
        self.particle_sprite.rect = self.particle_rect

        self.particle_image = pygame.Surface((self.particle_rect.w, self.particle_rect.h))
        self.particle_image.fill((255, 125, 0))
        self.particle_image2 = pygame.Surface((self.particle_rect.h, self.particle_rect.w))
        self.particle_image2.fill((255, 125, 0))

        self.particle_sprite.image = self.particle_image

        self.collision_rect = self.rect.inflate(-self.rect.w * 0.7, -self.rect.h * 0.25)

        self.dx = 0
        self.dy = 0

        self.orig_pos = None

    def vyser_particle(self, particle_id):
        self.particles.add(LightParticle(particle_id, self))

    def update(self):
        self.particle_origin = self.rect.center
        self.collision_rect.center = self.rect.center

        if self.direction == 0:
            self.particle_sprite.image = self.particle_image
            self.particle_rect.w = 250
            self.particle_rect.h = 60
            self.particle_rect.left = self.rect.center[0]
            self.particle_rect.top = self.rect.center[1] - 30
        elif self.direction == 180:
            self.particle_sprite.image = self.particle_image
            self.particle_rect.w = 250
            self.particle_rect.h = 60
            self.particle_rect.right = self.rect.center[0]
            self.particle_rect.top = self.rect.center[1] - 30
        if self.direction == 90:
            self.particle_sprite.image = self.particle_image2
            self.particle_rect.w = 60
            self.particle_rect.h = 250
            self.particle_rect.left = self.rect.center[0] - 30
            self.particle_rect.top = self.rect.center[1]
        elif self.direction == 270:
            self.particle_sprite.image = self.particle_image2
            self.particle_rect.w = 60
            self.particle_rect.h = 250
            self.particle_rect.left = self.rect.center[0] - 30
            self.particle_rect.bottom = self.rect.center[1]

        super().update()

        # compute deltas
        self.dx = self.rect.centerx - self.last_position[0]
        self.dy = self.rect.centery - self.last_position[1]

        if self.dx > 0:
            self.direction = 0
        elif self.dx < 0:
            self.direction = 180
        elif self.dy > 0:
            self.direction = 90
        elif self.dy < 0:
            self.direction = 270

        # update last position
        self.last_position = self.rect.center

        if len(self.particles) + len(self.removed_particles) < config.LIGHT_PARTICLE_COUNT:
            for i in range(config.LIGHT_PARTICLE_BATCH_SIZE):
                self.vyser_particle(i)
