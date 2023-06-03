import unittest

from game.models.components.bot import BotDifficulty
from game.models.components.ship import Ship
from game.models.game_model import GameModel
from game.models.components.player import Player, ResultAttack
from game.models.settings_model import SettingsModel


class MockPlayer(Player):
    def __init__(self):
        super().__init__()
        self.opponent_moves = []

    def fire(self, x: int, y: int) -> ResultAttack:
        return self.opponent_moves.pop(0)


class GameModelTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = MockPlayer()
        self.player1.place_ship(Ship((0, 0), 1, 2))
        self.player2 = MockPlayer()
        self.player2.place_ship(Ship((5, 5), 1, 2))
        self.game_model = GameModel(self.player1, self.player2)

    def test_update(self):
        pos = (2, 3)
        result = ResultAttack.HIT

        self.game_model.update(pos, result)

        self.assertEqual(self.player1.opponent_board[2][3].is_hit(), True)
        self.assertIsNone(self.game_model.get_winner())

        self.assertEqual(self.game_model.move_player, self.player1)
        self.assertEqual(self.game_model.sleep_player, self.player2)

    def test_make_move(self):
        self.player2.opponent_moves = [ResultAttack.MISS]

        pos = (4, 5)
        self.game_model.make_move(pos)

        self.assertEqual(self.player2.opponent_board[4][5].is_hit(), False)
        self.assertIsNone(self.game_model.get_winner())

        self.assertEqual(self.game_model.move_player, self.player2)
        self.assertEqual(self.game_model.sleep_player, self.player1)

    def test_switch_players(self):
        self.assertEqual(self.game_model.move_player, self.player1)
        self.assertEqual(self.game_model.sleep_player, self.player2)

        self.game_model.switch_players()

        self.assertEqual(self.game_model.move_player, self.player2)
        self.assertEqual(self.game_model.sleep_player, self.player1)

    def test_is_game_over(self):
        self.assertFalse(self.game_model.is_game_over())

        self.player1.ships = []
        self.assertTrue(self.game_model.is_game_over())

        self.player2.time = 0
        self.assertTrue(self.game_model.is_game_over())

    def test_get_winner(self):
        self.assertIsNone(self.game_model.get_winner())

        self.player1.ships = []
        self.game_model.check_game_over()
        self.assertEqual(self.game_model.get_winner(), self.player2)

        self.player2.time = 0
        self.assertEqual(self.game_model.get_winner(), self.player2)


class SettingsModelTestCase(unittest.TestCase):
    def setUp(self):
        self.settings_model = SettingsModel()

    def test_set_default_settings(self):
        self.settings_model.set_default_settings()

        self.assertEqual(self.settings_model.get_board_size(), (10, 10))
        self.assertEqual(self.settings_model.get_ships(),
                         [(1, 1), (1, 2), (1, 3), (1, 4)])
        self.assertAlmostEqual(self.settings_model.get_bot_speed(), 0.0001)
        self.assertEqual(self.settings_model.get_bot_level(),
                         BotDifficulty.SMART)

    def test_set_default_board_size(self):
        self.settings_model.set_default_board_size()

        self.assertEqual(self.settings_model.get_board_size(), (10, 10))

    def test_set_default_ship(self):
        self.settings_model.set_default_ship()

        self.assertEqual(self.settings_model.get_ships(),
                         [(1, 1), (1, 2), (1, 3), (1, 4)])

    def test_set_default_bot_speed(self):
        self.settings_model.set_default_bot_speed()

        self.assertAlmostEqual(self.settings_model.get_bot_speed(), 0.0001)

    def test_set_default_bot_level(self):
        self.settings_model.set_default_bot_level()

        self.assertEqual(self.settings_model.get_bot_level(),
                         BotDifficulty.SMART)

    def test_set_bot_speed(self):
        self.settings_model.set_bot_speed(0.00001)
        self.assertAlmostEqual(self.settings_model.get_bot_speed(), 0.00001)

        self.settings_model.set_bot_speed(0.001)
        self.assertAlmostEqual(self.settings_model.get_bot_speed(), 0.001)

    def test_set_board_size(self):
        self.settings_model.set_board_size((8, 8))
        self.assertEqual(self.settings_model.get_board_size(), (8, 8))

        self.settings_model.set_board_size((0, 10))
        self.assertEqual(self.settings_model.get_board_size(), (10, 10))

        self.settings_model.set_board_size((10, -1))
        self.assertEqual(self.settings_model.get_board_size(), (10, 10))

    def test_is_correct_ship(self):
        self.settings_model.set_board_size((10, 10))

        self.assertTrue(self.settings_model.is_correct_ship((1, 1)))
        self.assertTrue(self.settings_model.is_correct_ship((5, 5)))
        self.assertFalse(self.settings_model.is_correct_ship((10, 11)))
        self.assertFalse(self.settings_model.is_correct_ship((11, 10)))

    def test_set_ships(self):
        self.settings_model.set_ships([(1, 1), (2, 2), (3, 3)])

        self.assertEqual(self.settings_model.get_ships(),
                         [(1, 1), (2, 2), (3, 3)])

        self.settings_model.set_ships([(1, 1), (11, 11)])

        self.assertEqual(self.settings_model.get_ships(), [(1, 1)])

    def test_set_bot_level(self):
        self.settings_model.set_bot_level(BotDifficulty.EASY)
        self.assertEqual(self.settings_model.get_bot_level(),
                         BotDifficulty.EASY)

        self.settings_model.set_bot_level(BotDifficulty.SMART)
        self.assertEqual(self.settings_model.get_bot_level(),
                         BotDifficulty.SMART)


if __name__ == '__main__':
    unittest.main()
