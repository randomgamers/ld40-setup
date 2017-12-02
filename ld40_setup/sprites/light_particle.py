import pygame
from .. import utils, config
import math


class LightParticle(pygame.sprite.Sprite):
    def __init__(self, particle_id, parent):
        super().__init__()

        self.parent = parent
        self.particle_id = particle_id

        self.size = 16
        self.position = [100, 100]

        # self.type = random.randint(0, 2)

        # if self.type == 0:
        self.image, self.rect = utils.load_image('particles/particle.png', use_alpha=True)
        self.original_image = self.image.copy()

        self.speed = config.LIGHT_PARTICLE_SPEED  # random.randrange(16, 24)
        self.lifetime = 0
        self.reset()

    def reset(self):
        self.visible = True

        self.image = self.original_image.copy()

        # self.parent.speed_x > 0 && self.parent.speed_y > 0
        direction = self.parent.direction - config.LIGHT_PARTICLE_ANGLE/2 + (self.particle_id / config.LIGHT_PARTICLE_BATCH_SIZE) * config.LIGHT_PARTICLE_ANGLE

        self.speed_x = self.speed * math.cos(math.radians(direction))
        self.speed_y = self.speed * math.sin(math.radians(direction))

        self.rect.center = self.parent.rect.center
        self.lifetime = config.LIGHT_PARTICLE_LIFETIME

    def check_collisions(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            self.visible = False

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)
        size_const = 1 + 3 * (1 - (self.lifetime / config.LIGHT_PARTICLE_LIFETIME))

        self.image = pygame.transform.scale(self.original_image, (int(self.size * size_const), int(self.size * size_const)))
        self.lifetime -= 1

        if self.lifetime == 1:
            self.reset()
