import pygame

from game.components.cell import CellWithShip


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
                rect = pygame.Rect(x * self.cell_width + self.x,
                                   y * self.cell_height + self.y,
                                   self.cell_width, self.cell_height)
                if isinstance(cell, CellWithShip):
                    if cell.is_hit():
                        pygame.draw.rect(window, self.color_hit, rect)
                    else:
                        pygame.draw.rect(window, self.color_ship, rect)
                elif cell.is_hit():
                    pygame.draw.rect(window, self.color_miss, rect)
                else:
                    pygame.draw.rect(window, self.color_unknown, rect)
                pygame.draw.rect(window, (0, 0, 0),
                                 (x * self.cell_width + self.x,
                                  y * self.cell_height + self.y,
                                  self.cell_width, self.cell_height), 1)
        pygame.draw.rect(window, (0, 0, 0), self.frame_board, 2)

    def get_cell_pos(self, pos: (int, int)):
        return (int((pos[0] - self.x) // self.cell_width),
                int((pos[1] - self.y) // self.cell_height))
