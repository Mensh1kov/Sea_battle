import pygame

from SeaBattle.components import CellWithShip, Bot
from SeaBattle.logic import GameLogic


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
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


class MainMenuDisplay:
    def __init__(self):
        self.bg_color = (255, 255, 255)
        self.play_vs_bot_button = Button('One player', 300, 137, 200, 50, (0, 255, 0), (0, 200, 0))
        self.play_vs_player_button = Button('Two players', 300, 210, 200, 50, (0, 255, 0), (0, 200, 0))
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


class Board:
    def __init__(self, x, y, board_array):
        self.x = x
        self.y = y
        self.main_size = 350
        self.frame_board = pygame.Rect(x, y, self.main_size, self.main_size)
        self.width = len(board_array[0])
        self.height = len(board_array)
        self.cell_width = self.main_size / self.width
        self.cell_height = self.main_size / self.height
        self.board_array = board_array
        self.color_ship = (64, 64, 64)
        self.color_hit = (255, 0, 0)
        self.color_miss = (192, 192, 192)
        self.color_unknown = (255, 255, 255)

    def is_hovering(self, pos):
        return self.frame_board.collidepoint(pos)

    def render(self, window):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.board_array[y][x]
                rect = pygame.Rect(x * self.cell_width + self.x, y * self.cell_height + self.y, self.cell_width, self.cell_height)
                if isinstance(cell, CellWithShip):
                    if cell.is_hit():
                        pygame.draw.rect(window, self.color_hit, rect)
                    else:
                        pygame.draw.rect(window, self.color_ship, rect)
                elif cell.is_hit():
                    pygame.draw.rect(window, self.color_miss, rect)
                else:
                    pygame.draw.rect(window, self.color_unknown, rect)
                pygame.draw.rect(window, (0, 0, 0), (x * self.cell_width + self.x, y * self.cell_height + self.y, self.cell_width, self.cell_height), 1)
        pygame.draw.rect(window, (0, 0, 0), self.frame_board, 2)

    def get_cell_pos(self, pos):
        return int((pos[0] - self.x) // self.cell_width), int((pos[1] - self.y) // self.cell_height)


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
        text_surface = self.font.render(self.name_winner, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.text_pos)
        window.blit(text_surface, text_rect)
        self.back_to_menu_button.render(window)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_to_menu_button.is_hovering(event.pos):
                self.back_to_menu_button.action()


class GameDisplay:
    def __init__(self, game_logic: GameLogic):
        self.game_logic = game_logic
        self.left_board = Board(30, 40, game_logic.move_player.board)
        self.right_board = Board(30 + 350 + 40, 40, game_logic.move_player.opponent_board)
        self.bg_color = (255, 255, 255)
        self.game_over_action = None

    def render(self, window):
        if self.game_logic.winner:
            self.game_over_action(self.game_logic.winner.name)

        window.fill((255, 255, 255))
        self.left_board.render(window)
        self.right_board.render(window)

    def set_game_over_action(self, action):
        self.game_over_action = action

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not isinstance(self.game_logic.move_player, Bot) and self.right_board.is_hovering(event.pos):
                self.game_logic.move_player.set_move(self.right_board.get_cell_pos(event.pos))

