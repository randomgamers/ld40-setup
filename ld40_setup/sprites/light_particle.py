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

        # Make the collision rect slightly bigger
        self.collision_rect = self.rect.copy()

        self.speed = config.LIGHT_PARTICLE_SPEED  # random.randrange(16, 24)
        self.lifetime = 0
        self.reset()

    def reset(self):
        if not self.parent.particles.has(self):
            self.parent.particles.add(self)

        self.image = self.original_image.copy()

        # self.parent.speed_x > 0 && self.parent.speed_y > 0
        direction = self.parent.direction - config.LIGHT_PARTICLE_ANGLE/2 + (self.particle_id / (config.LIGHT_PARTICLE_BATCH_SIZE - 1)) * config.LIGHT_PARTICLE_ANGLE

        self.speed_x = self.speed * math.cos(math.radians(direction)) + self.parent.dx
        self.speed_y = self.speed * math.sin(math.radians(direction)) + self.parent.dy

        self.rect.center = self.parent.particle_origin
        self.lifetime = config.LIGHT_PARTICLE_LIFETIME

    def update(self, level):
        wall_check_points = [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]
        for check_point in wall_check_points:
            tile_x = int(check_point[0] / config.TILE_SIZE)
            tile_y = int(check_point[1] / config.TILE_SIZE)

            if tile_y >= len(level.map) or tile_y < 0:
                continue
            if tile_x >= len(level.map[tile_y]) or tile_x < 0:
                continue

            if level.map[tile_y][tile_x] == 'W':
                self.parent.particles.remove(self)
                break

        self.rect.move_ip(self.speed_x, self.speed_y)
        size_const = 1 + 3 * (1 - (self.lifetime / config.LIGHT_PARTICLE_LIFETIME))

        self.image = pygame.transform.scale(self.original_image, (int(self.size * size_const), int(self.size * size_const)))
        self.lifetime -= 1

        self.collision_rect = self.image.get_rect()
        self.collision_rect.center = self.rect.center

        if self.lifetime == 1:
            self.reset()
