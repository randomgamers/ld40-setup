import pygame

from ld40_setup import config


class Menu:

    def __init__(self, screen, menu_items, background_color,
                 message, message_size=config.MESSAGE_SIZE, message_color=config.MESSAGE_COLOR,
                 title_size=config.TITLE_SIZE, title_color=config.TITLE_COLOR,
                 item_size=config.ITEM_SIZE, item_color=config.ITEM_COLOR,
                 font=None):

        # save stuff
        self.screen = screen
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

        self.background_color = background_color
        self.clock = pygame.time.Clock()

        self.items = []

        # title
        title_font = font or pygame.font.Font(None, title_size)
        title_label = title_font.render(config.GAME_NAME, 1, title_color)
        label_width = title_label.get_rect().width
        label_height = title_label.get_rect().height
        label_position_x = (self.screen_width / 2) - (label_width / 2)
        label_position_y = self.screen_height / 4
        self.items.append([config.GAME_NAME, title_label, (label_width, label_height), (label_position_x, label_position_y)])

        # message
        message_font = font or pygame.font.Font(None, message_size)
        message_label = message_font.render(message, 1, message_color)
        label_width = message_label.get_rect().width
        label_height = message_label.get_rect().height
        label_position_x = (self.screen_width / 2) - (label_width / 2)
        label_position_y = 3 * self.screen_height / 8
        self.items.append([message, message_label, (label_width, label_height), (label_position_x, label_position_y)])

        # menu items
        item_font = font or pygame.font.Font(None, item_size)
        for index, item in enumerate(menu_items):
            label = item_font.render(item, 1, item_color)
            label_width = label.get_rect().width
            label_height = label.get_rect().height

            label_position_x = (self.screen_width / 2) - (label_width / 2)
            text_block_height = len(menu_items) * label_height
            label_position_y = (self.screen_height / 2) - (text_block_height / 2) + (index * label_height)

            self.items.append([item, label, (label_width, label_height), (label_position_x, label_position_y)])

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            return 'start'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return 'quit'
        elif event.type == pygame.QUIT:
            return 'quit'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'quit'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            return 'fullscreen'
        return None

    def show(self):
        result = None
        while result is None:
            self.clock.tick(config.FPS)

            # check keyboard
            for event in pygame.event.get():
                result = self.event_handler(event)

            # render the background
            self.screen.fill(self.background_color)

            # render menu items
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
        return result


class MainMenu(Menu):
    def __init__(self, screen):
        items = ['(S) Start', '(F) Fullscreen', '(Q) Quit']
        super().__init__(screen, menu_items=items, background_color=(40, 42, 56),
                         message='Main Menu')


class SuccessMenu(Menu):

    def __init__(self, screen, num_level):
        items = ['(S) Next Level', '(Q) Main Menu']
        super().__init__(screen, menu_items=items, background_color=(44,51,38),
                         message='Level #{} Complete'.format(num_level))


class FailureMenu(Menu):

    def __init__(self, screen, num_level):
        items = ['(S) Try Again', '(Q) Main Menu']
        super().__init__(screen, menu_items=items, background_color=(59,37,37),
                         message = 'Level #{} Failed'.format(num_level))


class GameWonMenu(Menu):

    def __init__(self, screen):
        items = ['(S) Play Whole Game Again', '(Q) Main Menu']
        super().__init__(screen, menu_items=items, background_color=(128,97,37), title_color=(0,0,0),
                         message='Game Completed')
