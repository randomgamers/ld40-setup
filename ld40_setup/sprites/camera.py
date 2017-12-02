from .rotating_sprite import RotatingSprite


class Camera(RotatingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='',
                         image_file='camera_small.png',
                         **kwargs)
