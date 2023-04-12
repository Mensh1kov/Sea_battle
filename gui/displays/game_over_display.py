import pygame

from gui.displays.widgets.button import Button


class GameOverDisplay:
    def __init__(self, name_winner):
        self.font = pygame.font.Font(None, 32)
        self.name_winner = name_winner
        self.bg_rect = pygame.Rect(250, 100, 300, 200)
        self.bg_rect_center = self.bg_rect.center
        self.text_pos = self.bg_rect_center[0], self.bg_rect_center[1] - 30
        self.back_to_menu_button = Button('Menu',
                                          self.bg_rect_center[0] - 100,
                                          self.bg_rect_center[1] + 10,
                                          200, 50, (0, 255, 0), (0, 200, 0))

    def render(self, window):
        pygame.draw.rect(window, (0, 102, 0), self.bg_rect)
        text_surface = self.font.render(self.name_winner, True,
                                        (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.text_pos)
        window.blit(text_surface, text_rect)
        self.back_to_menu_button.render(window)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_to_menu_button.is_hovering(event.pos):
                self.back_to_menu_button.action()
