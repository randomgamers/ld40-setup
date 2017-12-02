import os

from . import config


class Level:
    def __init__(self, level_num: int):
        level_file = os.path.join(config.PROJECT_ROOT, config.RESOURCES_ROOT, config.LEVELS_DIR,
                                  'level{}.map'.format(level_num))

        with open(level_file, 'r') as fin:
            self._char_map = [line.split() for line in fin]

    @property
    def map(self):
        return self._char_map


if __name__ == '__main__':
    level1 = Level(1)
    print(level1.map)
