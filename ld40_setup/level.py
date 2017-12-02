import os

from . import config


class Level:
    def __init__(self, level_num: int):
        level_file = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.LEVELS_DIR,
                                  'level{}.map'.format(level_num))

        with open(level_file, 'r') as fin:
            self.map = [list(line)[:-1] for line in fin]

        self.wall_coords = [(row_num, col_num) for row_num, row in enumerate(self.map)
                                               for col_num, tile in enumerate(row)
                                               if tile == 'W']

        self.entry_coords = [(row_num, col_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'E']

        self.doors_coords = [(row_num, col_num) for row_num, row in enumerate(self.map)
                                                for col_num, tile in enumerate(row)
                                                if tile == 'D']


if __name__ == '__main__':
    level1 = Level(1)
    print(level1.map)
    print(level1.wall_coords)
    print(level1.entry_coords)
    print(level1.doors_coords)
