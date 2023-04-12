import itertools
import random
import time
from enum import Enum

from game.components.player import Player


class BotDifficulty(Enum):
    EASY = 1
    SMART = 2


class Bot(Player):
    def __init__(self, speed: float = 0.1,
                 difficulty: BotDifficulty = BotDifficulty.EASY):
        super(Bot, self).__init__(name='Bot')
        self.speed = speed
        self.difficulty = difficulty
        self.available_moves = list(
            itertools.product(range(len(self.board[0])),
                              range(len(self.board))))

    def get_move(self) -> (int, int):
        if self.difficulty == BotDifficulty.EASY:
            return self.get_random_move()
        else:
            return self.get_smart_move()

    def get_random_move(self) -> (int, int):
        time.sleep(self.speed)

        if len(self.available_moves) == 0:
            return None

        pos = random.choice(self.available_moves)
        self.available_moves.remove(pos)
        return pos

    def get_smart_move(self) -> (int, int):
        pass
