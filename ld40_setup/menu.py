import pygame

from ld40_setup import config


class Menu:

    def __init__(self, screen, items, bg_color, font_size, message, font_color=(255, 255, 255), font=None):
        # save stuff
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 48)
        self.font_color = font_color

        self.items = []

        # title
        title_label = self.font.render(config.GAME_NAME, 1, font_color)
        label_width = title_label.get_rect().width
        label_height = title_label.get_rect().height
        label_position_x = (self.scr_width / 2) - (label_width / 2)
        label_position_y = self.scr_height / 4
        self.items.append([config.GAME_NAME, title_label, (label_width, label_height), (label_position_x, label_position_y)])

        # message
        title_label = self.font.render(message, 1, font_color)
        label_width = title_label.get_rect().width
        label_height = title_label.get_rect().height
        label_position_x = (self.scr_width / 2) - (label_width / 2)
        label_position_y = 3 * self.scr_height / 8
        self.items.append([message, title_label, (label_width, label_height), (label_position_x, label_position_y)])

        # generate menu items
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
            label_width = label.get_rect().width
            label_height = label.get_rect().height

            label_position_x = (self.scr_width / 2) - (label_width / 2)
            text_block_height = len(items) * label_height
            label_position_y = (self.scr_height / 2) - (text_block_height / 2) + (index * label_height)

            self.items.append([item, label, (label_width, label_height), (label_position_x, label_position_y)])

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            return 'start'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return 'quit'
        return None

    def show(self):
        result = None
        while result is None:
            self.clock.tick(config.FPS)

            # check keyboard
            for event in pygame.event.get():
                result = self.event_handler(event)

            # render the background
            self.screen.fill(self.bg_color)

            # render menu items
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
        return result


class MainMenu(Menu):
    def __init__(self, screen):
        items = ['(S) Start', '(Q) Quit']
        super().__init__(screen, items=items, bg_color=(0,0,0), font_size=30, message='Main Menu')


class SuccessMenu(Menu):

    def __init__(self, screen, num_level):
        items = ['(S) Next Level', '(Q) Main Menu']
        super().__init__(screen, items=items, bg_color=(0,0,0), font_size=30,
                         message='Level #{} Complete'.format(num_level))


class FailureMenu(Menu):

    def __init__(self, screen, num_level):
        items = ['(S) Try Again', '(Q) Main Menu']
        super().__init__(screen, items=items, bg_color=(0,0,0), font_size=30,
                         message = 'Level #{} Failed'.format(num_level))


class GameWonMenu(Menu):

    def __init__(self, screen):
        items = ['(S) Play Whole Game Again', '(Q) Main Menu']
        super().__init__(screen, items=items, bg_color=(0,0,0), font_size=30, message='Game Completed')
