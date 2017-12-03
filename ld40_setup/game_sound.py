from .utils import load_sound


class GameSound:
    def __init__(self, filename):
        self.sound = load_sound(filename)

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()

    @property
    def length(self):
        return self.sound.get_length()
