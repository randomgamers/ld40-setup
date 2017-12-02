import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 20))
        self.image.convert()
        self.image.fill((50, 50, 50))

        self.rect = self.image.get_rect()
        print(x, y)
        self.rect.move_ip(x*20, y*20)
