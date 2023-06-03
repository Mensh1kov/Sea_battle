import copy

from game.models.components.bot import BotDifficulty


class SettingsModel:
    def __init__(self):
        self._ships = None
        self._board_size = None
        self._bot_speed = None
        self._bot_level = None

        self.set_default_settings()

    def set_default_settings(self):
        self.set_default_board_size()
        self.set_default_ship()
        self.set_default_bot_speed()
        self.set_default_bot_level()

    def set_default_board_size(self):
        self._board_size = (10, 10)

    def set_default_ship(self):
        self._ships = [
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4)
        ]

    def set_default_bot_speed(self):
        self._bot_speed = .0001

    def set_default_bot_level(self):
        self._bot_level = BotDifficulty.SMART

    def set_bot_speed(self, speed: float):
        if speed > .001:
            self.set_default_bot_speed()
        else:
            self._bot_speed = speed

    def set_board_size(self, size: (int, int)):
        if size[0] <= 0 or size[1] <= 0:
            self.set_default_board_size()
        else:
            self._board_size = size

    def is_correct_ship(self, size_ship: (int, int)) -> bool:
        return self._board_size[0] >= size_ship[0] \
               and self._board_size[1] >= size_ship[1]

    def set_ships(self, ships: list[(int, int)]):
        self._ships = list(filter(self.is_correct_ship, ships))
        if len(self._ships) == 0:
            self.set_default_ship()

    def set_bot_level(self, level: BotDifficulty):
        self._bot_level = level

    def get_ships(self) -> list[(int, int)]:
        return copy.deepcopy(self._ships)

    def get_bot_speed(self) -> float:
        return self._bot_speed

    def get_board_size(self) -> (int, int):
        return self._board_size

    def get_bot_level(self) -> BotDifficulty:
        return self._bot_level
