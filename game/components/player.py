from enum import Enum
from game.components.cell import Cell, CellWithShip
from game.components.ship import Ship


class ResultAttack(Enum):
    MISS = 1
    HIT = 2
    SUNK = 3
    ATTACKED = 4
    ERROR = 5


class Player:
    def __init__(self, width_board: int = 10,
                 height_board: int = 10, name: str = 'Player'):
        self.name = name
        self.ships = []
        self.width_board = width_board
        self.height_board = height_board
        self.board = [[Cell() for _ in range(self.width_board)]
                      for _ in range(self.height_board)]
        self.opponent_board = [[Cell() for _ in range(self.width_board)]
                               for _ in range(self.height_board)]
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
            cell = self.board[y][x]
        except IndexError:
            return ResultAttack.ERROR

        if cell.is_hit():
            return ResultAttack.ATTACKED

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
        if result != ResultAttack.MISS and result != ResultAttack.ATTACKED:
            cell = CellWithShip(Ship(1, 1))
            cell.set_hit(True)
            self.opponent_board[y][x] = cell
        else:
            self.opponent_board[y][x].set_hit(True)
