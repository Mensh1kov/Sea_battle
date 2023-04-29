from game.components.bot import BotDifficulty


class SettingsModel:
    def __init__(self):
        self._ships = None
        self._board_size = None
        self._bot_speed = None
        self._bot_level = None

        self.set_default_settings()

    def set_default_settings(self):
        self._board_size: (int, int) = (10, 10)
        self._ships: list[tuple[int, int, int]] = [
            (1, 1, 4),
            (1, 2, 3),
            (1, 3, 2),
            (1, 4, 1)
        ]
        self._bot_speed: float = 0.0001
        self._bot_level = BotDifficulty.SMART

    def set_bot_speed(self, speed: float):
        self._bot_speed = speed

    def set_board_size(self, size: (int, int)):
        self._board_size = size

    def set_ships(self, ships: list[tuple[int, int, int]]):
        self._ships = ships

    def set_bot_level(self, level: BotDifficulty):
        self._bot_level = level

    def get_ships(self) -> list[tuple[int, int, int]]:
        return self._ships

    def get_bot_speed(self) -> float:
        return self._bot_speed

    def get_board_size(self) -> (int, int):
        return self._board_size

    def get_bot_level(self) -> BotDifficulty:
        return self._bot_level