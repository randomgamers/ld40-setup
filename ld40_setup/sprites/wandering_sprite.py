from typing import List, Tuple

import numpy as np

from .animated_sprite import AnimatedSprite


class WanderingSprite(AnimatedSprite):
    """Sprite following a path back and forth."""

    def __init__(self, walk_path: List[Tuple[int, int]], walk_speed: int, **kwargs):
        assert len(walk_path) > 1
        self.walk_path = walk_path

        super().__init__(position=self.walk_path[0], **kwargs)

        self.path_progress = 0
        self.path_forward = True
        self.next_tile_to = self.walk_path[1]

        self.walk_speed = walk_speed
        self.update_speed()

    def next_path_part(self):
        if self.path_forward:
            if self.path_progress == len(self.walk_path) - 1:
                self.path_forward = False
                self.next_tile_to = self.walk_path[len(self.walk_path) - 2]
            else:
                self.next_tile_to = self.walk_path[self.path_progress + 1]
                self.path_progress += 1
        else:
            if self.path_progress == 0:
                self.path_forward = True
                self.next_tile_to = self.walk_path[1]
            else:
                self.next_tile_to = self.walk_path[self.path_progress - 1]
                self.path_progress -= 1

    def update_speed(self):
        tile_current = self.current_tile
        self.speed_x = self.walk_speed * np.sign(self.next_tile_to[0] - tile_current[0])
        self.speed_y = self.walk_speed * np.sign(self.next_tile_to[1] - tile_current[1])

    def update(self):
        super().update()

        # update path progress
        if self.next_tile_to == self.current_tile:
            self.next_path_part()
            self.update_speed()
