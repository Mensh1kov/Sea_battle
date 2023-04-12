import pygame


class Button:
    def __init__(self, text, x, y, width, height, color,
                 hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 32)

    def render(self, window):
        if self.is_hovering(pygame.mouse.get_pos()):
            pygame.draw.rect(window, self.hover_color, self.rect)
        else:
            pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_hovering(self, pos):
        return self.rect.collidepoint(pos)

    def set_action(self, action):
        self.action = action
