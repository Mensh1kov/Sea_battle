import itertools
import random
import time
from enum import Enum

from SeaBattle.settings import Settings


class Ship:
    def __init__(self, width: int, length: int):
        self.width = width
        self.length = length
        self.size = width * length
        self.hits = 0

    def is_sunk(self) -> bool:
        return self.hits == self.size


class Cell:
    def __init__(self):
        self.hit = False

    def is_hit(self) -> bool:
        return self.hit

    def set_hit(self, hit: bool):
        self.hit = hit


class ResultAttack(Enum):
    MISS = 1
    HIT = 2
    SUNK = 3
    ALREADY_ATTACKED = 4
    ERROR = 5


class CellWithShip(Cell):
    def __init__(self, ship: Ship):
        super().__init__()
        self.ship = ship

    def get_ship(self) -> Ship:
        return self.ship


class Player:
    def __init__(self, name: str):
        self.name = name
        self.ships = []
        self.board = [[Cell() for _ in range(Settings.board_size)]
                      for _ in range(Settings.board_size)]
        self.opponent_board = [[Cell() for _ in range(Settings.board_size)]
                               for _ in range(Settings.board_size)]
        self.__move = None

    def set_move(self, pos: (int, int)):
        self.__move = pos

    def get_move(self) -> (int, int):
        move = self.__move
        self.__move = None
        return move

    def place_ship(self, ship: Ship, x: int, y: int, horizontal=False) -> bool:
        width = ship.width
        length = ship.length

        if horizontal:
            width, length = length, width

        for i in range(width):
            for j in range(length):
                if x + i > 9 or y + j > 9:
                    return False
                if isinstance(self.board[y + j][x + i], CellWithShip):
                    return False

        for i in range(width):
            for j in range(length):
                self.board[y + j][x + i] = CellWithShip(ship)

        self.ships.append(ship)
        return True

    def fire(self, x: int, y: int) -> ResultAttack:
        try:
            cell = self.board[x][y]
        except IndexError:
            return ResultAttack.ERROR

        if cell.is_hit():
            return ResultAttack.ALREADY_ATTACKED

        if isinstance(cell, CellWithShip):
            ship = cell.get_ship()
            ship.hits += 1
            cell.set_hit(True)

            if ship.is_sunk():
                self.ships.remove(ship)
                return ResultAttack.SUNK
            return ResultAttack.HIT
        cell.set_hit(True)
        return ResultAttack.MISS

    def is_loser(self) -> bool:
        return not bool(len(self.ships))

    def update_opponent_board(self, x: int, y: int, result: ResultAttack):
        if result != ResultAttack.MISS and result != ResultAttack.ALREADY_ATTACKED:
            cell = CellWithShip(Ship(1, 1))
            cell.set_hit(True)
            self.opponent_board[y][x] = cell
        else:
            self.opponent_board[y][x].set_hit(True)


class Bot(Player):
    def __init__(self):
        super(Bot, self).__init__('Bot')
        self.available_moves = list(
            itertools.product(range(len(self.board[0])),
                              range(len(self.board))))

    def get_move(self) -> (int, int):
        time.sleep(Settings.bot_speed)

        if len(self.available_moves) == 0:
            raise Exception('нет доступных ходов')

        pos = random.choice(self.available_moves)
        self.available_moves.remove(pos)
        return pos
