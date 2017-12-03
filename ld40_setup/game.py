import pygame
from pygame.locals import *
from pygame.compat import geterror
import sys
import os
import numpy as np
import time

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

from .utils import load_sound, load_image, coord_to_game_pixel, game_pixel_to_coord, dist, init_screen, toggle_fullscreen, fullscreen
# from .sprites import Fist
from .level import get_level_classes
from .game_camera import GameCamera
from . import config
from .menu import MainMenu, SuccessMenu, FailureMenu, GameWonMenu


def scale_window_to_screen(window, screen):
    pygame.transform.scale(window, screen.get_size(), screen)


def blit_game_to_window(game_screen, window, camera):
    window.blit(game_screen, pygame.Rect(*camera.blit_position, *window.get_size()))


def character_collided_with_light(character, particle):
    return character.light_collision_rect.colliderect(particle.collision_rect)


def check_for_detection(character, cameraguard, screen_collision_box):
    # Check collision with guards light beam
    if cameraguard.particle_rect.colliderect(screen_collision_box) and pygame.sprite.collide_rect(cameraguard.particle_sprite, character):
        if pygame.sprite.spritecollideany(character, cameraguard.particles, collided=character_collided_with_light):
            return True
    # Check for collision with the guard himself
    if cameraguard.collision_rect.colliderect(character.light_collision_rect):
        return True
    return False


def main():
    # Initialize Everything
    pygame.mixer.pre_init(44100, -16, 1, 512) # Including this makes the sound not lag
    pygame.init()

    pygame.display.set_caption(config.GAME_NAME)
    pygame.mouse.set_visible(0)
    screen = init_screen(False)
    level_classes = get_level_classes()
    max_levels = len(level_classes)

    # show game menu until quit
    while True:

        # Main Menu
        response = MainMenu(screen).show()
        if response == 'quit': break
        elif response == 'start': pass
        else: raise ValueError('unknown menu response: {}'.format(response))

        won_levels = 0

        # foreach level
        for level_num, level_class in enumerate(level_classes, 1):

            # show success
            if level_num > 1:
                response = SuccessMenu(screen, level_num-1).show()
                if response == 'quit':
                    time.sleep(config.AFTER_QUIT_DELAY)
                    break
                elif response == 'start': pass
                else: raise ValueError('unknown menu response: {}'.format(response))

            go_to_menu = False  # player doesnt want to continue playing the level and want to go back to menu

            # while level not finished
            while True:
                success = play_level(level_class(), screen)  # play the fame
                if success:  # continue to next level
                    won_levels += 1
                    break
                else:  # show failure menu
                    response = FailureMenu(screen, level_num).show()
                    if response == 'quit':
                        time.sleep(config.AFTER_QUIT_DELAY)
                        go_to_menu = True
                        break
                    elif response == 'start': pass
                    else: raise ValueError('unknown menu response: {}'.format(response))

            if go_to_menu:  # player didnt want to replay the level
                break

        if won_levels == max_levels:
            response = GameWonMenu(screen).show()
            if response == 'quit':
                time.sleep(config.AFTER_QUIT_DELAY)
                break
            elif response == 'start': pass
            else: raise ValueError('unknown menu response: {}'.format(response))

    pygame.quit()  # terminate gracefully


def play_level(level, screen):
    total_hostages = len(level.hostages)

    tiles = config.TILES

    game_size = list(map(lambda shape: shape * config.TILE_SIZE, level.map_shape))
    game_screen = pygame.Surface(game_size)
    base_game_screen = pygame.Surface(game_size)

    window_size = tiles[0] * config.TILE_SIZE, tiles[1] * config.TILE_SIZE
    window = pygame.Surface(window_size)

    camera = GameCamera(game_size, window_size)

    pygame.mixer.init()

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

    # fist = Fist(camera)

    floor = pygame.sprite.Group(*level.floor)
    walls = pygame.sprite.Group(*level.walls)
    doors = pygame.sprite.Group(*level.doors)

    base_game_screen.blit(background, (0, 0))
    floor.draw(base_game_screen)
    walls.draw(base_game_screen)
    doors.draw(base_game_screen)

    guards = pygame.sprite.Group(*level.guards)
    cameras = pygame.sprite.Group(*level.cameras)
    shit_with_light = pygame.sprite.Group(*level.guards, *level.cameras)
    hostages = pygame.sprite.Group(*level.hostages)
    soundwaves = pygame.sprite.Group(*list(map(lambda h: h.soundwave, hostages)))
    player = level.player
    # allsprites = pygame.sprite.RenderPlain((player, fist))  # player.collision_sprite, guards.sprites()[0].particle_sprite
    allsprites = pygame.sprite.RenderPlain(player)  # player.collision_sprite, guards.sprites()[0].particle_sprite

    busted_blue = pygame.Surface(screen.get_size())
    busted_blue = busted_blue.convert_alpha()
    busted_blue.fill((180, 20, 20, 128))

    busted, busted_rect = load_image('busted.png', use_alpha=True)

    # Main Loop
    going = True
    pygame.key.set_repeat(1, int(1000 / config.FPS))

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                screen = toggle_fullscreen(screen)
            # elif event.type == MOUSEBUTTONDOWN:
            #     if fist.punch(player):
            #         punch_sound.play()  # punch
            #     else:
            #         whiff_sound.play()  # miss
            # elif event.type == MOUSEBUTTONUP:
            #     fist.unpunch()


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

        if not player.busted:
            allsprites.update()
            guards.update()
            cameras.update()

            screen_collision_box = pygame.Rect((np.array(camera.blit_position) * -1), (window.get_size()))
            for cameraguard in shit_with_light.sprites():
                cameraguard.particles.update(level)
                cameraguard.removed_particles.update(level)

                if check_for_detection(player, cameraguard, screen_collision_box):
                    player.busted = True
                for hostage in player.train:
                    if check_for_detection(hostage, cameraguard, screen_collision_box):
                        player.busted = True

            hostages.update()
            soundwaves.update()
            # This can be probably written more effectively but YOLO
            for hostage in player.train:
                for guard in guards.sprites():
                    if dist(hostage.rect.center, guard.rect.center) < hostage.soundwave_radius:
                        player.busted = True

            # if pygame.sprite.groupcollide(soundwaves, guards, dokilla=False, dokillb=False):
            #     player.busted = True
        else:
            player_pos = player.rect.center
            should_die_soon = False
            for guard in guards.sprites():
                if guard.orig_pos is None:
                    guard.orig_pos = guard.rect.center

                abs_dist = abs(guard.rect.centerx - player_pos[0]) + abs(guard.rect.centery - player_pos[1])
                if abs_dist < 1.5 * config.TILE_SIZE:
                    should_die_soon = True

                dx = int(float(guard.orig_pos[0] - player_pos[0]) / float(config.FPS))
                dy = int(float(guard.orig_pos[1] - player_pos[1]) / float(config.FPS))

                if not should_die_soon:
                    guard.rect.center = guard.rect.centerx - dx, guard.rect.centery - dy

            if should_die_soon:
                player.dead_count += 1
                if player.dead_count >= (2 * config.FPS):
                    player.dead = True

        camera.update()

        # Draw Everything
        # Blit base game screen to game screen
        game_screen.blit(base_game_screen, (0, 0))

        for cameraguard in shit_with_light.sprites():
            if cameraguard.particle_rect.colliderect(screen_collision_box):
                cameraguard.particles.draw(game_screen)

        guards.draw(game_screen)
        cameras.draw(game_screen)
        soundwaves.draw(game_screen)
        hostages.draw(game_screen)

        allsprites.draw(game_screen)
        # player.particles.draw(game_screen)

        # render texts
        for name, label, (width, height), (posx, posy) in level.texts:
            game_screen.blit(label, (posx, posy))

        # copy gamescreen to screen
        blit_game_to_window(game_screen, window, camera)
        scale_window_to_screen(window, screen)

        if player.dead_count > 0:
            screen.blit(busted_blue, (0, 0))
            screen.blit(busted, (screen.get_size()[0] / 2 - busted_rect.w / 2, screen.get_size()[1] / 2 - busted_rect.h / 2))

        # render FPS counter
        font = pygame.font.Font(None, 48)
        fps_text = font.render("%.2f" % (1000.0/delay), 1, (10, 10, 10))
        fps_text_pos = fps_text.get_rect()
        fps_text_pos.topleft = (0, 0)
        screen.blit(fps_text, fps_text_pos)

        pygame.display.flip()


if __name__ == '__main__':
    main()

# import cProfile as profile
# profile.run('main()', 'profile.txt')
