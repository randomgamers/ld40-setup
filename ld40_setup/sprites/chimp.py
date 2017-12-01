import pygame
from ..utils import load_image, load_image_norect
from .. import config


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        # self.image, self.rect = load_image('chimp.bmp', -1)

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

        self.image_index = 0

        self.frame_wait_counter = 0
        self.frame_wait_max = config.FPS
        self.frame_wait_max /= len(self.images)
        self.frame_wait_max /= 3

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.speed_x = 0
        self.speed_y = 0
        self.dizzy = 0
        self.walking = False


    def update(self):
        # sprite update
        if self.walking :
            self.frame_wait_counter += 1
            if self.frame_wait_counter >= self.frame_wait_max:
                self.frame_wait_counter = 0
                self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0

            # flipping hoizontally
            if self.speed_x < 0:
                self.image = pygame.transform.flip(self.images[self.image_index], True, False)
            else :
                self.image = self.images[self.image_index]

        # if self.dizzy:
        #     self._spin()
        # else:
        #     self._walk()

    def _walk(self):
        newpos = self.rect.move((self.speed_x, self.speed_y))
        self.rect = newpos

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
