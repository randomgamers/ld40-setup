from .utils import load_sound


class GameSound:
    def __init__(self, filename):
        self.sound = load_sound(filename)

    def play(self, loops=0):
        self.sound.play(loops)

    def stop(self):
        self.sound.stop()

    @property
    def length(self):
        return self.sound.get_length()

    def set_volume(self, volume):
        return self.sound.set_volume(volume)
