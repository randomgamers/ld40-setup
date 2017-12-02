from typing import Tuple
import pygame

from .animated_sprite import AnimatedSprite


class Hostage(AnimatedSprite):
    def __init__(self, image_dir, image_files, position, player):
        super().__init__(image_dir=image_dir, image_files=image_files, position=position)

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

    def collision_check(self, _, player):
        return self.collision_rect.colliderect(player.rect)

    def update(self):
        self.speed_x = self.speed_y = 0
        super().update()
        self.collision_rect.center = self.rect.center

        collisions = pygame.sprite.spritecollide(self, [self.player], False, collided=self.collision_check)
        if collisions:
            for collision in collisions:
                if not self.in_train:
                    self.player.add_to_train(self)
                    self.in_train = True
                # x_offset = self.collision_rect.center[0] - collision.rect.center[0]
                # y_offset = self.collision_rect.center[1] - collision.rect.center[1]
                # x_offset_threshold = self.collision_rect.w / 2
                # y_offset_threshold = self.collision_rect.h / 2
                # if abs(x_offset) - config.TILE_SIZE/2 < x_offset_threshold and abs(y_offset) - config.TILE_SIZE/2 < y_offset_threshold*0.5:
                #     direction = 'left' if x_offset > 0 else 'right'
                #     self.allowed_directions[direction] = False
                # if abs(y_offset) - config.TILE_SIZE/2 < y_offset_threshold and abs(x_offset) - config.TILE_SIZE/2 < x_offset_threshold*0.25:
                #     direction = 'top' if y_offset > 0 else 'bottom'
                #     self.allowed_directions[direction] = False

    def move_to(self, new_position: Tuple[int,int]):
        self.rect.center = self.collision_rect.center = new_position


class NoisyChick(Hostage):
    def __init__(self, position, player):
        super().__init__(image_dir='characters/hostage1/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         position=position,
                         player=player)
