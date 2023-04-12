import pygame

from game.components.bot import Bot
from gui.displays.widgets.board import Board
from game.logic import GameLogic


class GameDisplay:
    def __init__(self, game_logic: GameLogic):
        self.game_logic = game_logic
        self.left_board = Board(30, 40, game_logic.move_player.board)
        self.right_board = Board(30 + 350 + 40, 40,
                                 game_logic.move_player.opponent_board)
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
            if not isinstance(self.game_logic.move_player, Bot) \
                    and self.right_board.is_hovering(event.pos):
                self.game_logic.move_player.set_move(
                    self.right_board.get_cell_pos(event.pos))
