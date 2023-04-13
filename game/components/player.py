import random
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

    def place_ships_randomly(self, ships: list[Ship]):
        for ship in ships:
            placed = False
            while not placed:
                x = random.randint(0, self.width_board - 1)
                y = random.randint(0, self.height_board - 1)
                horizontal = random.choice([True, False])
                placed = self.place_ship(ship, x, y, horizontal)

    def place_ship(self, ship: Ship, x: int, y: int, horizontal=False) -> bool:
        width = ship.width
        length = ship.length

        if horizontal:
            width, length = length, width

        for i in range(max(0, x - 1), min(x + width + 1, self.width_board)):
            for j in range(max(0, y - 1), min(y + length + 1,
                                              self.height_board)):
                if isinstance(self.board[j][i], CellWithShip):
                    return False

        if x + width > self.width_board or y + length > self.height_board:
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
