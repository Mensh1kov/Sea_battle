import random
from enum import Enum
from typing import Union

from game.components.cell import Cell, CellWithShip
from game.components.ship import Ship


class ResultAttack(Enum):
    MISS = 1
    HIT = 2
    SUNK = 3
    ATTACKED = 4
    ERROR = 5


class Player:
    def __init__(self, board_size: (int, int) = (10, 10),
                 name: str = 'Player'):
        self.name = name
        self.ships = []
        self.width_board = board_size[0]
        self.height_board = board_size[1]
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

    def place_ships_randomly(self, ships: list[(int, int)]):
        for width, height in ships:
            placed = False
            while not placed:
                x = random.randint(0, self.width_board - 1)
                y = random.randint(0, self.height_board - 1)
                horizontal = random.choice([True, False])
                placed = self.place_ship(Ship((x, y), width,
                                              height, horizontal))

    def place_ship(self, ship: Ship) -> bool:
        width = ship.width
        length = ship.length
        x = ship.pos[0]
        y = ship.pos[1]

        if ship.horizontal:
            width, length = length, width

        for i in range(max(0, x - 1), min(x + length + 1, self.height_board)):
            for j in range(max(0, y - 1), min(y + width + 1,
                                              self.width_board)):
                if isinstance(self.board[i][j], CellWithShip):
                    return False

        if y + width > self.width_board or x + length > self.height_board:
            return False

        for i in range(length):
            for j in range(width):
                self.board[x + i][y + j] = CellWithShip(ship)

        self.ships.append(ship)
        return True

    def fire(self, x: int, y: int) -> ResultAttack:
        try:
            cell = self.board[x][y]
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

    def remove_ship(self, pos: (int, int)) -> Union[None, Ship]:
        try:
            cell = self.board[pos[0]][pos[1]]
        except IndexError:
            return None

        if isinstance(cell, CellWithShip):
            ship = cell.get_ship()
            self.ships.remove(ship)
            width = ship.width
            length = ship.length

            if ship.horizontal:
                width, length = length, width

            for i in range(length):
                for j in range(width):
                    self.board[i + ship.pos[0]][j + ship.pos[1]] = Cell()
            return ship

    def update_opponent_board(self, x: int, y: int, result: ResultAttack):
        if result != ResultAttack.MISS and result != ResultAttack.ATTACKED:
            cell = CellWithShip(Ship((x, y), 1, 1))
            cell.set_hit(True)
            self.opponent_board[x][y] = cell
        else:
            self.opponent_board[x][y].set_hit(True)

    def set_name(self, name: str):
        self.name = name
