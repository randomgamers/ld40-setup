import os
import numpy as np

from . import config
from .sprites import Player, hostages, Guard, Camera, Wall, Floor


class Level:
    def __init__(self):
        assert hasattr(self, 'level_num')

        level_file = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.LEVELS_DIR,
                                  'level{}.map'.format(self.level_num))

        with open(level_file, 'r') as fin:
            self.map = [list(line)[:-1] for line in fin]

        self.wall_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                               for col_num, tile in enumerate(row)
                                               if tile == 'W']
        self.walls = []
        for x, y in self.wall_coords:
            wall = Wall(x, y)
            self.walls.append(wall)

        self.entry_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'E']

        assert len(self.entry_coords) == 1, 'Too many/few level entries'

        self.doors_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'D']

        self.floor_coords = [(col_num, row_num) for row_num, row in enumerate(self.map)
                             for col_num, tile in enumerate(row)
                             if tile == '.']

        self.floor = []
        for x, y in self.floor_coords:
            floor_tile = Floor(x, y)
            self.floor.append(floor_tile)

        self.player = Player(position=self.entry_coords[0], walls=self.walls)
        self.guards = []
        self.hostages = []

    @property
    def map_shape(self):
        return np.array(self.map).T.shape


def build_level(level_num: int) -> Level:
    return [Level1][level_num-1]()


class Level1(Level):
    def __init__(self):
        self.level_num = 1

        super().__init__()

        self.guards = [
            Guard(walk_path=[(2,6), (10,6)], walk_speed=1),
            Camera(position=(2,15), angle_from=-180, angle_to=0, rotation_speed=60, delay=1),
        ]

        self.hostages = [
            hostages.NoisyChick(position=(5,5), player=self.player),
            hostages.FatGuy(position=(7,7), player=self.player),
        ]

