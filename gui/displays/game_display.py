import abc
from game.logic import GameLogic
from gui.displays.display import Display


class GameDisplay(Display, metaclass=abc.ABCMeta):
    def __init__(self, size: (int, int), game_logic: GameLogic):
        super().__init__(size)
        self.game_logic = game_logic
        self.bg_color = (255, 255, 255)
        self.game_over_action = None

    def set_game_over_action(self, action):
        self.game_over_action = action
