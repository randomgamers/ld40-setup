import math
from . import config


class Camera(object):
    def __init__(self, game_size, window_size):
        self.game_size = game_size
        self.window_size = window_size
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.wanted_position = [0, 0]

    def update(self):
        pos_diff = [float(self.wanted_position[i] - self.position[i]) for i in (0, 1)]
        distance = float(math.sqrt(pos_diff[0] ** 2 + pos_diff[1] ** 2))

        current_velocity = float(config.CAMERA_VELOCITY * distance / config.MAX_CAMERA_DISTANCE)
        for ax in (0, 1):
            self.velocity[ax] = current_velocity * pos_diff[ax] / distance
            self.position[ax] = self.position[ax] + self.velocity[ax]

    @property
    def blit_position(self):
        pos0 = -self.position[0] + self.window_size[0] / 2
        pos1 = -self.position[1] + self.window_size[1] / 2

        max_pos0 = -self.game_size[0] + self.window_size[0]
        max_pos1 = -self.game_size[1] + self.window_size[1]

        return max(max_pos0, min(0, pos0)), max(max_pos1, min(0, pos1))
