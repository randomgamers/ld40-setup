from .rotating_sprite import RotatingSprite


class Camera(RotatingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='runsprite',
                         image_file='run001.png',
                         **kwargs)
