from .wandering_sprite import WanderingSprite


class Guard(WanderingSprite):

    def __init__(self, **kwargs):
        super().__init__(image_dir='characters/hostage1/walk',
                         image_files=['walk_0{}.png'.format(i) for i in range(1, 9)],
                         **kwargs)
