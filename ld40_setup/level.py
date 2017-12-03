import os
import numpy as np
from typing import List, Type

import pygame

from . import config
from .sprites import Player, hostages, Guard, Camera, Wall, Floor, Door
from .utils import coord_to_game_pixel


class Level:
    def __init__(self):
        assert hasattr(self, 'level_num')

        # load level
        level_file = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.LEVELS_DIR,
                                  'level{}.map'.format(self.level_num))

        with open(level_file, 'r') as fin:
            self.map = [list(line)[:-1] for line in fin]

        # build walls
        self.wall_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                               for col_num, tile in enumerate(row)
                                               if tile == 'W']
        self.walls = [Wall(x, y) for x, y in self.wall_coords]

        # select entry coord
        self.entry_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'E']
        assert len(self.entry_coords) == 1, 'Too many/few level entries'
        self.entry_coord = self.entry_coords[0]

        self.end_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in
                                                enumerate(row) if tile == ',']

        # build doors
        self.doors_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'D' or tile == 'F' or tile == 'G']
        self.doors = [Door(x, y, self.map[y][x]) for x, y in self.doors_coords]

        # build floor
        self.floor_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                             for col_num, tile in enumerate(row)
                             if tile == '.' or tile == ',']

        self.floor = []
        for x, y in self.floor_coords:
            floor_tile = Floor(x, y, self.map[y][x])
            self.floor.append(floor_tile)



        self.entry_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'E']
        assert len(self.entry_coords) == 1, 'Too many/few level entries'
        self.entry_coord = self.entry_coords[0]

        entry_tile = Floor(self.entry_coord[0], self.entry_coord[1])
        self.floor.append(entry_tile)

        # player
        self.player = Player(position=(self.entry_coord[0], self.entry_coord[1] - 0.5), walls=self.walls)

        # sprites
        self.guards = []
        self.cameras = []
        self.hostages = []
        self.texts = []

        # text config
        self.font = pygame.font.Font(None, config.INGAME_TEXT_SIZE)

    def add_text(self, message, position):
        label = self.font.render(message, 1, config.INGAME_TEXT_COLOR)
        width = label.get_rect().width
        height = label.get_rect().height
        px_position = coord_to_game_pixel(position)
        self.texts.append([message, label, (width, height), px_position])

    @property
    def map_shape(self):
        return np.array(self.map).T.shape


def get_level_classes() -> List[Type[Level]]:
    return [
        Level1,
        Level2,
        Level3,
        Level4,
    ]


class Level1(Level):
    def __init__(self):
        self.level_num = 1
        super().__init__()

        self.hostages = [
            hostages.NoisyChick(position=(16, 2), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.FatGuy(position=(46, 11), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(17, 8), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(17, 11), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords)
        ]

        self.cameras = [
            Camera(position=(38.5, 3.5), angle_from=270, angle_to=271, rotation_speed=1, delay=1),
        ]

        self.guards = [
            Guard(walk_path=[(28, 8), (28, 11)], walk_speed=1),
        ]

        self.add_text('This is the', (1, 2))
        self.add_text('safety zone.', (1, 2.5))

        self.add_text('Let\'s get all four', (1, 4))
        self.add_text('hostages here as', (1, 4.5))
        self.add_text('fast as possible.', (1, 5))

        self.add_text('Seems like a', (15, 3))
        self.add_text('kidnapped lady.', (15, 3.5))
        self.add_text('Take her to safety!', (15, 4.5))

        self.add_text('Some hostages are', (27, 3))
        self.add_text('pretty loud and', (27, 3.5))
        self.add_text('may attract attention.', (27, 4))

        self.add_text('There\'s a camera', (33, 3))
        self.add_text('on the right.', (33, 3.5))
        self.add_text('Don\'t let it see you!', (33, 4))

        self.add_text('Oh, the second hostage!', (44, 8.5))
        self.add_text('Such a fat guy,', (44, 9))
        self.add_text('bet he\'s very slow.', (44, 9.5))

        self.add_text('What a dangerous guard!', (32, 11))
        self.add_text('Better watch his moves', (32, 11.5))
        self.add_text('before you pass him.', (32, 12))

        self.add_text('The final hostages! Let\'s', (19, 8))
        self.add_text('take them home together.', (19, 8.5))
        self.add_text('Hostages will form a line', (19, 9.5))
        self.add_text('following your steps.', (19, 10))
        self.add_text('The more you have it', (19, 10.5))
        self.add_text('the harder the escape is.', (19, 11))


class Level2(Level):
    def __init__(self):
        self.level_num = 2

        super().__init__()

        self.guards = [
            Guard(walk_path=[(2,3), (11,3)], walk_speed=2),
            Guard(walk_path=[(11,5), (2,5)], walk_speed=2),
            Guard(walk_path=[(2,7), (11,7)], walk_speed=2),
            Guard(walk_path=[(26,7), (16,7), (16,5), (26,5), (26,3), (16,3)], walk_speed=7),
        ]

        self.hostages = [
            hostages.FatGuy(position=(1, 1), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.NoisyChick(position=(13, 1), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.NoisyChick(position=(15, 1), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.FatGuy(position=(27, 1), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
        ]


class Level3(Level):
    def __init__(self):
        self.level_num = 3

        super().__init__()

        self.guards = [
            Guard(walk_path=[(1,7), (1,14)], walk_speed=2),
            Guard(walk_path=[(31,7), (31,14)], walk_speed=2),
            Guard(walk_path=[(12,11), (19,11)], walk_speed=5),
        ]

        self.hostages = [
            hostages.RegularGuy(position=(3, 15), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(29, 15), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(13, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.FatGuy(position=(14, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(15, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.NoisyChick(position=(16, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(17, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(18, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.FatGuy(position=(19, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(20, 17), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
        ]


class Level4(Level):
    def __init__(self):
        self.level_num = 4

        super().__init__()

        self.guards = [
            Guard(walk_path=[(3, 21), (25, 21)], walk_speed=3),
            Guard(walk_path=[(32, 14), (32, 19)], walk_speed=2),
            Guard(walk_path=[(57, 19), (57, 14)], walk_speed=2),
            Guard(walk_path=[(35, 20), (50, 20)], walk_speed=5),
            Guard(walk_path=[(50, 11), (50, 6)], walk_speed=3),
            Guard(walk_path=[(43, 6), (43, 11)], walk_speed=3),
            Guard(walk_path=[(34, 11), (34, 6)], walk_speed=3),
        ]

        self.cameras = [
            Camera(position=(0.5, 12), angle_from=-90, angle_to=90, rotation_speed=70, delay=2),
            Camera(position=(8.5, 25), angle_from=-45, angle_to=45, rotation_speed=50, delay=1.5),
            Camera(position=(35, 21.5), angle_from=170, angle_to=260, rotation_speed=60, delay=1),
            Camera(position=(43.5, 15), angle_from=0, angle_to=90, rotation_speed=30, delay=1)
        ]

        self.hostages = [
            hostages.RegularGuy(position=(8, 10), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(26, 25), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(58, 23), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
            hostages.RegularGuy(position=(19, 10), player=self.player, entry_tile=self.entry_coord, end_tiles=self.end_coords),
        ]
