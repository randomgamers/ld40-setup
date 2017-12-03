import pygame
from pygame.locals import *
from pygame.compat import geterror
import sys
import os
import numpy as np

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

from .utils import load_sound, coord_to_game_pixel
from .sprites import Fist
from .level import build_level
from .game_camera import GameCamera
from . import config
from .menu import MainMenu


def scale_window_to_screen(window, screen):
    pygame.transform.scale(window, screen.get_size(), screen)


def blit_game_to_window(game_screen, window, camera):
    window.blit(game_screen, pygame.Rect(*camera.blit_position, *window.get_size()))


def main():
    # Initialize Everything
    pygame.mixer.pre_init(44100, -16, 1, 512) # Including this makes the sound not lag
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    pygame.display.set_caption(config.GAME_NAME)
    pygame.mouse.set_visible(0)

    response = MainMenu(screen).run()
    if response == 'quit':
        quit()
    elif response == 'start':
        pass

    # foreach level
    max_levels = 3
    for level_num in range(1, max_levels+1):

        # while level not finished
        # show_menu(level_num, 'pre', screen)
        while True:
            success = play_level(level_num, screen)
            if success:
                break
            else:
                pass
                # show_menu(level_num, 'fail', screen)

    # show_menu(-1, 'finished', screen)

    pygame.quit()


def play_level(level_num, screen):
    level = build_level(level_num)
    total_hostages = len(level.hostages)

    tiles = config.TILES

    game_size = list(map(lambda shape: shape * config.TILE_SIZE, level.map_shape))
    game_screen = pygame.Surface(game_size)
    window_size = tiles[0] * config.TILE_SIZE, tiles[1] * config.TILE_SIZE
    window = pygame.Surface(window_size)

    camera = GameCamera(game_size, window_size)

    # Create The Backgound
    background = pygame.Surface(game_screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display The Background
    game_screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')

    fist = Fist(camera)

    floor = pygame.sprite.Group(*level.floor)
    walls = pygame.sprite.Group(*level.walls)
    guards = pygame.sprite.Group(*level.guards)
    hostages = pygame.sprite.Group(*level.hostages)
    player = level.player
    allsprites = pygame.sprite.RenderPlain((player, fist)) # player.collision_sprite, guards.sprites()[0].particle_sprite

    # Main Loop
    going = True
    pygame.key.set_repeat(1, int(1000 / config.FPS));

    while going:
        delay = clock.tick(config.FPS)

        if total_hostages == player.num_saved_hostages:
            return True

        if player.dead:
            return False

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(player):
                    punch_sound.play()  # punch
                else:
                    whiff_sound.play()  # miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        player.stop_walk()
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            player.move_y(-1)
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            player.move_y(1)
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            player.move_x(-1)
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            player.move_x(1)

        camera.wanted_position = player.rect.center

        allsprites.update()
        guards.update()
        for guard in guards.sprites():
            guard.particles.update(level)
            screen_rect = pygame.Rect((np.array(camera.blit_position)*-1), (window.get_size()))

            if guard.particle_rect.colliderect(screen_rect) and pygame.sprite.collide_rect(guard.particle_sprite, player):
                pass #playerwas detected by guard

        hostages.update()
        for hostage in hostages.sprites():
            hostage.soundwaves.update()
        camera.update()

        # Draw Everything
        game_screen.blit(background, (0, 0))
        floor.draw(game_screen)
        walls.draw(game_screen)
        screen_rect = pygame.Rect((np.array(camera.blit_position) * -1), (window.get_size()))
        for guard in guards.sprites():
            if guard.particle_rect.colliderect(screen_rect):
                for particle in guard.particles.sprites():
                    if particle.visible:
                        pygame.sprite.GroupSingle(particle).draw(game_screen)
        guards.draw(game_screen)
        for hostage in hostages.sprites():
            hostage.soundwaves.draw(game_screen)
            # if hostage.soundwave_rect.colliderect(screen_rect):
        hostages.draw(game_screen)
        #
        # for hostage in hostages.sprites():
        #     for circle in hostage.soundwaves:
        #         if circle['radius'] > 3:
        #             pygame.draw.circle(game_screen, (255, 0, 0, 100) , hostage.rect.center, circle['radius'], 3)

        allsprites.draw(game_screen)
        # player.particles.draw(game_screen)

        blit_game_to_window(game_screen, window, camera)
        scale_window_to_screen(window, screen)

        font = pygame.font.Font(None, 48)
        fps_text = font.render("%.2f" % (1000.0/delay), 1, (10, 10, 10))
        fps_text_pos = fps_text.get_rect()
        fps_text_pos.topleft = (0, 0)
        screen.blit(fps_text, fps_text_pos)

        pygame.display.flip()
    # quit()   #TODO: without this the game cannot be terminated


if __name__ == '__main__':
    main()
