import unittest

from game.models.components.bot import Bot, Status
from game.models.components.player import ResultAttack, Player
from game.models.components.cell import Cell, CellWithShip
from game.models.components.ship import Ship


class BotTestCase(unittest.TestCase):
    def setUp(self):
        self.board_size = (10, 10)
        self.bot = Bot(self.board_size)

    def test_get_random_move(self):
        move = self.bot.get_random_move()
        self.assertNotIn(move, self.bot.available_moves)

    def test_get_smart_move(self):
        self.bot.set_bot_status(Status.ATTACK)
        self.bot.update_opponent_board(2, 2, ResultAttack.HIT)

        move = self.bot.get_smart_move()
        self.assertNotIn(move, self.bot.available_moves)

    def test_update_opponent_board(self):
        x = 5
        y = 5
        result = ResultAttack.HIT

        self.bot.update_opponent_board(x, y, result)
        self.assertEqual(self.bot.last_move_pos, (x, y))
        self.assertEqual(self.bot.last_move_result, result)
        self.assertIn((x, y), self.bot.hits)


class CellTestCase(unittest.TestCase):
    def test_is_hit(self):
        cell = Cell()
        self.assertFalse(cell.is_hit())

    def test_set_hit(self):
        cell = Cell()
        cell.set_hit(True)
        self.assertTrue(cell.is_hit())
        cell.set_hit(False)
        self.assertFalse(cell.is_hit())


class CellWithShipTestCase(unittest.TestCase):
    def test_get_ship(self):
        ship = Ship((1, 1), 1, 3)
        cell = CellWithShip(ship)
        self.assertEqual(cell.get_ship(), ship)


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player((10, 10), 'Player')

    def test_set_move(self):
        self.player.set_move((2, 3))
        move = self.player.get_move()
        self.assertEqual(move, (2, 3))
        self.assertIsNone(self.player.get_move())

    def test_place_ship(self):
        ship1 = Ship((0, 0), 2, 3, True)
        ship2 = Ship((2, 2), 3, 2, False)

        self.assertTrue(self.player.place_ship(ship1))
        self.assertFalse(self.player.place_ship(ship2))

    def test_get_ship(self):
        ship = Ship((0, 0), 2, 3, True)
        self.player.place_ship(ship)

        self.assertEqual(self.player.get_ship((0, 0)), ship)
        self.assertIsNone(self.player.get_ship((5, 5)))

    def test_fire(self):
        ship = Ship((2, 2), 1, 2, True)
        self.player.place_ship(ship)

        result = self.player.fire(2, 2)
        self.assertEqual(result, ResultAttack.HIT)

        result = self.player.fire(2, 3)
        self.assertEqual(result, ResultAttack.SUNK)

        result = self.player.fire(4, 2)
        self.assertEqual(result, ResultAttack.MISS)

        result = self.player.fire(2, 2)
        self.assertEqual(result, ResultAttack.ATTACKED)

        result = self.player.fire(100, 100)
        self.assertEqual(result, ResultAttack.ERROR)

    def test_is_loser(self):
        self.assertTrue(self.player.is_loser())

        ship = Ship((0, 0), 2, 3, True)
        self.player.place_ship(ship)
        self.assertFalse(self.player.is_loser())

        self.player.time = 0
        self.assertTrue(self.player.is_loser())

    def test_remove_ship(self):
        ship = Ship((1, 1), 2, 2, True)
        self.player.place_ship(ship)

        removed_ship = self.player.remove_ship((1, 1))
        self.assertEqual(removed_ship, ship)
        self.assertNotIn(ship, self.player.ships)

        removed_ship = self.player.remove_ship((5, 5))
        self.assertIsNone(removed_ship)

    def test_update_opponent_board(self):
        self.player.update_opponent_board(2, 3, ResultAttack.HIT)
        self.assertIsInstance(self.player.opponent_board[2][3], CellWithShip)
        self.assertTrue(self.player.opponent_board[2][3].is_hit())

        self.player.update_opponent_board(5, 5, ResultAttack.MISS)
        self.assertTrue(self.player.opponent_board[5][5].is_hit())

    def test_set_name(self):
        self.assertEqual(self.player.name, 'Player')
        self.player.set_name('New Player')
        self.assertEqual(self.player.name, 'New Player')


class ShipTestCase(unittest.TestCase):
    def setUp(self):
        self.ship = Ship((2, 2), 3, 2, True)

    def test_is_sunk(self):
        self.assertFalse(self.ship.is_sunk())

        self.ship.hits = 6
        self.assertTrue(self.ship.is_sunk())

    def test_set_horizontal(self):
        self.assertTrue(self.ship.horizontal)

        self.ship.set_horizontal(False)
        self.assertFalse(self.ship.horizontal)


if __name__ == '__main__':
    unittest.main()
