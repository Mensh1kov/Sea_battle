import pygame
from gui.displays.game_display import GameDisplay
from gui.displays.widgets.board import Board
from game.logic import GameLogic


class Text:
    def __init__(self, pos: (int, int), text: str,
                 font_size: int = 32,
                 color: (int, int, int) = (255, 255, 255)):
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect()
        # Это не очень хорошо, т.к. мы передаем позицию для размещения,
        # а эта позиция задается центру текста
        self.text_rect.center = pos

    def render(self, surface):
        surface.blit(self.text_surface, self.text_rect)


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
        x = wight // 2
        # не очень красивое решения для добавления подписи к доскам,
        # возможно сделать одну сущность, которая будет внутри себя
        # агрегировать и подпись и доску...
        self.r_name = Text((x * 3, 20), self.game_logic.move_player.name,
                           color=(255, 0, 0))
        self.l_name = Text((x, 20), self.game_logic.sleep_player.name,
                           color=(255, 0, 0))

    def render(self, surface):
        if self.game_logic.winner:
            self.game_over_action(self.game_logic.winner.name)

        surface.fill(self.bg_color)
        self.dict[self.game_logic.move_player]['signal'].render(surface)
        self.r_name.render(surface)
        self.l_name.render(surface)
        self.left_board.render(surface)
        self.right_board.render(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            board = self.dict[self.game_logic.move_player]['board']
            if board.is_hovering(event.pos):
                self.game_logic.move_player.set_move(
                    board.get_cell_pos(event.pos))
