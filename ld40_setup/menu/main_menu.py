import pygame

from .. import config


class MainMenu:
    def __init__(self, screen, bg_color=(0, 0, 0), font=None, font_size=30,
                 font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        items = ['(S) Start', '(ESC) Quit']
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def run(self):
        result = None
        while result is None:
            self.clock.tick(config.FPS)

            if pygame.key.get_pressed()[pygame.K_s]:
                result = 'start'
            if pygame.key.get_pressed()[pygame.K_q]:
                result = 'quit'

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    result = 'start'
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    result = 'quit'

            # Redraw the background
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
        return result
