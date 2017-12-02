import os
import numpy as np

from . import config
from .sprites import Player, hostages, Guard, Camera, Wall, Floor


class Level:
    def __init__(self, level_num: int):
        level_file = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.LEVELS_DIR,
                                  'level{}.map'.format(level_num))

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

        self.player = Player(self.walls)

        self.guards = [
            Guard(walk_path=[(2,6), (10,6), (10,10), (20,10)], walk_speed=1),
            Guard(walk_path=[(10,10), (20,10), (20, 15)], walk_speed=2),
            Camera(position=(12,3), angle_from=0, angle_to=90, rotation_speed=60, delay=1),
        ]

        self.hostages = [
            hostages.NoisyChick(position=(5,5), player=self.player),
            hostages.FatGuy(position=(7,7), player=self.player),
        ]



    @property
    def map_shape(self):
        return np.array(self.map).T.shape
