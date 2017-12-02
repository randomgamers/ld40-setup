from .wandering_sprite import WanderingSprite


class Guard(WanderingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='runsprite',
                         image_files=['run00{}.png'.format(i) for i in range(1, 9)],
                         **kwargs)
