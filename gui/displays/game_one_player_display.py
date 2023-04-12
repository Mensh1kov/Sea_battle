import pygame
from game.components.bot import Bot
from gui.displays.game_display import GameDisplay
from gui.displays.widgets.board import Board
from game.logic import GameLogic


class GameOnePlayerDisplay(GameDisplay):
    def __init__(self, size: (int, int), game_logic: GameLogic):
        super().__init__(size, game_logic)
        self.left_board = Board(30, 40, game_logic.move_player.board)
        self.right_board = Board(30 + 350 + 40, 40,
                                 game_logic.move_player.opponent_board)

    def render(self, surface):
        if self.game_logic.winner:
            self.game_over_action(self.game_logic.winner.name)

        surface.fill(self.bg_color)
        self.left_board.render(surface)
        self.right_board.render(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not isinstance(self.game_logic.move_player, Bot) \
                    and self.right_board.is_hovering(event.pos):
                self.game_logic.move_player.set_move(
                    self.right_board.get_cell_pos(event.pos))
