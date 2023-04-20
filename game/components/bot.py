import itertools
import random
import time
from enum import Enum
from game.components.player import Player, ResultAttack


class BotDifficulty(Enum):
    EASY = 1
    SMART = 2


class Status(Enum):
    SEARCH = 1
    ATTACK = 2


def move_position(x, y, direction):
    if direction == "up":
        y -= 1
    elif direction == "down":
        y += 1
    elif direction == "left":
        x -= 1
    elif direction == "right":
        x += 1
    elif direction == "up_right":
        x += 1
        y -= 1
    elif direction == "up_left":
        x -= 1
        y -= 1
    elif direction == "down_right":
        x += 1
        y += 1
    elif direction == "down_left":
        x -= 1
        y += 1

    return x, y


class Bot(Player):
    def __init__(self, board_size: (int, int), speed: float = 0.1,
                 difficulty: BotDifficulty = BotDifficulty.SMART):
        super(Bot, self).__init__(board_size, name='Bot')
        self.speed = speed
        self.difficulty = difficulty
        self.available_moves = list(
            itertools.product(range(len(self.board[0])),
                              range(len(self.board))))
        self.last_move_pos = None
        self.last_move_result = None
        self.directions = ["up", "down", "left", "right", "up_right",
                           "up_left", "down_right", "down_left"]
        self.direction = random.choice(self.directions)
        self.status = Status.SEARCH
        self.where_shoot = {}
        self.hits = []

    def get_move(self) -> (int, int):
        if self.difficulty == BotDifficulty.EASY:
            return self.get_random_move()
        else:
            return self.get_smart_move()

    def bot_setting(self):
        time.sleep(self.speed)

        if len(self.available_moves) == 0:
            return None

    def get_random_move(self) -> (int, int):
        self.bot_setting()

        pos = random.choice(self.available_moves)
        self.available_moves.remove(pos)
        return pos

    def set_bot_status(self, status: Status):
        self.status = status

    def determine_direction(self, x, y):
        for i in range(4):
            x1, y1 = move_position(x, y, self.directions[i])
            if (x1, y1) in self.available_moves:
                if (x1, y1) in self.where_shoot:
                    self.where_shoot[(x1, y1)] += 1
                else:
                    self.where_shoot[(x1, y1)] = 1

    def get_smart_move(self) -> (int, int):
        self.bot_setting()

        if self.last_move_result == ResultAttack.HIT:
            self.set_bot_status(Status.ATTACK)

        if self.last_move_result == ResultAttack.SUNK:

            for x, y in self.hits:
                for i in range(8):
                    x1, y1 = move_position(x, y, self.directions[i])
                    if (x1, y1) in self.available_moves:
                        self.available_moves.remove((x1, y1))

            self.hits.clear()
            self.where_shoot.clear()
            self.set_bot_status(Status.SEARCH)

        if self.status == Status.ATTACK:
            if self.last_move_result != ResultAttack.MISS:
                x, y = self.hits[-1]
                self.determine_direction(x, y)

            shoot_pos = max(self.where_shoot,
                            key=lambda pos: self.where_shoot[pos])
            del self.where_shoot[shoot_pos]

            if shoot_pos in self.available_moves:
                self.available_moves.remove(shoot_pos)
            return shoot_pos

        else:
            return self.get_random_move()

    def update_opponent_board(self, x: int, y: int, result: ResultAttack):
        self.last_move_pos = (x, y)
        self.last_move_result = result

        if result != ResultAttack.MISS and result != ResultAttack.ATTACKED:
            self.hits.append(self.last_move_pos)
    
