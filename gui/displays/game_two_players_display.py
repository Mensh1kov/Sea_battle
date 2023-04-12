import pygame
from gui.displays.game_display import GameDisplay
from gui.displays.widgets.board import Board
from game.logic import GameLogic


class Signal:
    def __init__(self, x: int, y: int, wight: int,
                 height: int, color: (int, int, int)):
        self.rect = pygame.Rect(x, y, wight, height)
        self.color = color

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)


class GameTwoPlayersDisplay(GameDisplay):
    def __init__(self, size: (int, int), game_logic: GameLogic):
        super().__init__(size, game_logic)
        self.left_board = Board(30, 40, game_logic.sleep_player.opponent_board)
        self.right_board = Board(30 + 350 + 40, 40,
                                 game_logic.move_player.opponent_board)
        sign_color = (0, 255, 0)
        wight = self.size[0] // 2
        height = self.size[1]
        self.dict = {game_logic.move_player: {'board': self.right_board,
                                              'signal': Signal(wight, 0,
                                                               wight, height,
                                                               sign_color)},
                     game_logic.sleep_player: {'board': self.left_board,
                                               'signal': Signal(0, 0,
                                                                wight, height,
                                                                sign_color)}}

    def render(self, surface):
        if self.game_logic.winner:
            self.game_over_action(self.game_logic.winner.name)

        surface.fill(self.bg_color)
        self.dict[self.game_logic.move_player]['signal'].render(surface)
        self.left_board.render(surface)
        self.right_board.render(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            board = self.dict[self.game_logic.move_player]['board']
            if board.is_hovering(event.pos):
                self.game_logic.move_player.set_move(
                    board.get_cell_pos(event.pos))
