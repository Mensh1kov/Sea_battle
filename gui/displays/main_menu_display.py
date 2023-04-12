import pygame

from gui.displays.widgets.button import Button


class MainMenuDisplay:
    def __init__(self):
        self.bg_color = (255, 255, 255)
        self.play_vs_bot_button = Button('One player', 300, 137, 200, 50,
                                         (0, 255, 0), (0, 200, 0))
        self.play_vs_player_button = Button('Two players', 300, 210, 200, 50,
                                            (0, 255, 0), (0, 200, 0))
        self.buttons = [self.play_vs_bot_button,
                        self.play_vs_player_button]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_hovering(event.pos):
                    if button.action:
                        button.action()

    def render(self, window):
        window.fill(self.bg_color)
        for button in self.buttons:
            button.render(window)