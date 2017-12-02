from typing import Tuple
import pygame

from .animated_sprite import AnimatedSprite


class Hostage(AnimatedSprite):
    def __init__(self, image_dir, image_files, position, player):
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
        self.collision_sprite = pygame.sprite.Sprite()
        self.collision_sprite.rect = self.collision_rect
        self.collision_sprite.image = pygame.Surface((self.collision_rect.w, self.collision_rect.h))
        self.collision_sprite.image.fill((255, 125, 0))

        # last speeds
        self.last_position = position

    def collision_check(self, _, player):
        return self.collision_rect.colliderect(player.rect)

    def update(self):

        # compute deltas
        dx = self.rect.centerx - self.last_position[0]
        dy = self.rect.centery - self.last_position[1]

        # update last position
        self.last_position = self.rect.center

        if dx != 0 or dy != 0:  # instead of super update
            print(dx, dy)
            self.animate()

        self.collision_rect.center = self.rect.center

        collisions = pygame.sprite.spritecollide(self, [self.player], False, collided=self.collision_check)
        if collisions:
            for collision in collisions:
                if not self.in_train:
                    self.player.add_to_train(self)
                    self.in_train = True

    def move_to(self, new_position: Tuple[int,int]):
        self.rect.center = self.collision_rect.center = new_position


class NoisyChick(Hostage):
    def __init__(self, position, player):
        super().__init__(image_dir='characters/hostage1/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position,
                         player=player)
        self.noise = 1


class FatGuy(Hostage):
    def __init__(self, position, player):
        super().__init__(image_dir='characters/hostage2/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position,
                         player=player)
        self.slowdown = 2
