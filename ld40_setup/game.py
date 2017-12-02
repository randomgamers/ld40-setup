import pygame
from pygame.locals import *
from pygame.compat import geterror
import sys
import os

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

from .utils import load_sound
from .sprites import Player, Fist, Wall
from .level import Level
from . import config
from .level import Level

def main():
    # Initialize Everything
    pygame.mixer.pre_init(44100, -16, 1, 512) # Including this makes the sound not lag
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    player = Player()
    fist = Fist()
    level = Level(1)
    allsprites = pygame.sprite.RenderPlain((player, fist))

    level1 = Level(1)
    walls = pygame.sprite.Group()
    for x, y in level1.wall_coords:
        wall = Wall(x, y)
        walls.add(wall)
        print(wall.rect)

    # Main Loop
    going = True
    pygame.key.set_repeat(1, int(1000 / config.FPS));
    while going:
        clock.tick(config.FPS)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                player.moveX(3);
            elif event.type == KEYDOWN and event.key == K_LEFT:
                player.moveX(-3);
            elif event.type == KEYDOWN and event.key == K_UP:
                player.moveY(-3);
            elif event.type == KEYDOWN and event.key == K_DOWN:
                player.moveY(3);
            elif event.type == KEYUP and event.key == K_RIGHT:
                player.moveX(0);
            elif event.type == KEYUP and event.key == K_LEFT:
                player.moveX(0);
            elif event.type == KEYUP and event.key == K_UP:
                player.moveY(0);
            elif event.type == KEYUP and event.key == K_DOWN:
                player.moveY(0);
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(player):
                    punch_sound.play()  # punch
                    player.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()
        # Draw Everything
        screen.blit(background, (0, 0))
        walls.draw(screen)
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
