import pygame
from ..utils import load_image, load_image_norect
from .. import config

class Player(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self, walls):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        # self.image, self.rect = load_image('chimp.bmp', -1)

        self.walls = walls

        self.images = []
        self.images.append(load_image_norect('runsprite/run001.png', -1))
        self.images.append(load_image_norect('runsprite/run002.png', -1))
        self.images.append(load_image_norect('runsprite/run003.png', -1))
        self.images.append(load_image_norect('runsprite/run004.png', -1))
        self.images.append(load_image_norect('runsprite/run005.png', -1))
        self.images.append(load_image_norect('runsprite/run006.png', -1))
        self.images.append(load_image_norect('runsprite/run007.png', -1))
        self.images.append(load_image_norect('runsprite/run008.png', -1))

        self.image, self.rect = load_image('runsprite/run001.png', -1)
        self.collision_rect = self.rect.inflate(-self.rect.w*0.52, -self.rect.h*0.35)

        self.collision_sprite = pygame.sprite.Sprite()
        self.collision_sprite.rect = self.collision_rect
        self.collision_sprite.image = pygame.Surface((self.collision_rect.w, self.collision_rect.h))
        self.collision_sprite.image.fill((255, 125, 0))

        self.image_index = 0

        self.frame_wait_counter = 0
        self.frame_wait_max = config.FPS
        self.frame_wait_max /= len(self.images)
        self.frame_wait_max /= 3

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.move_ip(60, 100)
        self.speed_x = 0
        self.speed_y = 0
        self.dizzy = 0
        self.walking = False

        self.allowed_directions = dict(left=True, right=True, top=True, bottom=True)

    def collision_check(self, _, wall):
        return self.collision_rect.colliderect(wall.rect)

    def update(self):
        # sprite update
        self.collision_rect.center = (self.rect.center[0], self.rect.center[1] + self.rect.w*0.1)

        for direction, _ in self.allowed_directions.items():
            self.allowed_directions[direction] = True

        collisions = pygame.sprite.spritecollide(self, self.walls, False, collided=self.collision_check)
        if collisions:
            for collision in collisions:
                x_offset = self.collision_rect.center[0] - collision.rect.center[0]
                y_offset = self.collision_rect.center[1] - collision.rect.center[1]
                x_offset_threshold = self.collision_rect.w / 2
                y_offset_threshold = self.collision_rect.h / 2
                if abs(x_offset) > x_offset_threshold and abs(y_offset) < y_offset_threshold*0.9:
                    direction = 'left' if x_offset > 0 else 'right'
                    self.allowed_directions[direction] = False
                if abs(y_offset) > y_offset_threshold and abs(x_offset) < x_offset_threshold*0.9:
                    direction = 'top' if y_offset > 0 else 'bottom'
                    self.allowed_directions[direction] = False

        if self.walking:
            self.frame_wait_counter += 1
            if self.frame_wait_counter >= self.frame_wait_max:
                self.frame_wait_counter = 0
                self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0

            # flipping hoizontally
            if self.speed_x < 0:
                self.image = pygame.transform.flip(self.images[self.image_index], True, False)
            elif self.speed_x > 0:
                self.image = self.images[self.image_index]

        # if self.dizzy:
        #     self._spin()
        # else:
        #     self._walk()

    def _walk(self):
        x_direction = 'left' if self.speed_x < 0 else 'right'
        y_direction = 'top' if self.speed_y < 0 else 'bottom'

        if not self.allowed_directions[x_direction]:
            self.speed_x = 0
        if not self.allowed_directions[y_direction]:
            self.speed_y = 0

        self.rect.move_ip((self.speed_x, self.speed_y))

    def moveX(self, speed):
        self.speed_x = speed
        self.updateWalk()

    def moveY(self, speed):
        self.speed_y = speed
        self.updateWalk()

    def updateWalk(self):
        if self.speed_x != 0 or self.speed_y != 0:
            self.walking = True
            self._walk()
        else :
            self.walking = False



    def stopWalk(self):
        self.walking = False

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
