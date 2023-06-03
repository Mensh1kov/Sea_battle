import sys
import unittest
from unittest.mock import MagicMock, call
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication

from game.controllers.placement_ships_controller import \
    PlacementShipsController
from game.controllers.settings_controller import SettingsController
from game.models.components.bot import BotDifficulty
from game.models.components.cell import Cell, CellWithShip
from game.models.components.player import Player
from game.models.components.ship import Ship
from game.models.game_model import GameModel
from game.models.settings_model import SettingsModel
from game.views.game_view import GameView
from game.views.placement_ships_view import PlacementShipsView
from game.views.settings_menu_view import SettingsMenuView
from game.views.widgets.board_and_player_widget import BoardAndPlayerWidget
from game.controllers.game_controller import GameController
from game.views.widgets.board_widget import BoardWidget


class GameControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.model = GameModel(Player((10, 10), "Player1"),
                               Player((10, 10), "Player2"))
        self.view = GameView()
        self.controller = GameController(self.model, self.view)
        self.controller.set_game_over_action(lambda: None)

    def tearDown(self):
        self.app.quit()
        self.app.deleteLater()

    def test_setup(self):
        self.assertIsNotNone(self.controller._timer)
        self.assertIsInstance(self.controller._timer, QTimer)
        self.assertEqual(self.controller._timer.interval(), 1000)

        self.assertEqual(self.controller._game_parts.keys(),
                         {self.model.move_player, self.model.sleep_player})
        self.assertIsInstance(
            self.controller._game_parts[self.model.move_player],
            BoardAndPlayerWidget)
        self.assertIsInstance(
            self.controller._game_parts[self.model.sleep_player],
            BoardAndPlayerWidget)

        self.assertIsNotNone(self.controller._game_over_action)

    def test_setup_timer(self):
        self.assertEqual(self.controller._timer.interval(), 1000)
        self.assertEqual(self.controller._timer.isActive(), True)
        self.assertIsNotNone(self.controller._timer.timeout)
        self.assertIsNotNone(self.controller._timer.timeout.connect)

    def test_setup_controller(self):
        self.assertEqual(self.controller._game_parts.keys(),
                         {self.model.move_player, self.model.sleep_player})
        self.assertIsInstance(
            self.controller._game_parts[self.model.move_player],
            BoardAndPlayerWidget)
        self.assertIsInstance(
            self.controller._game_parts[self.model.sleep_player],
            BoardAndPlayerWidget)

    def test_setup_view(self):
        self.assertIsInstance(
            self.controller._view.left_board_and_player.board, BoardWidget)
        self.assertIsInstance(
            self.controller._view.right_board_and_player.board, BoardWidget)

        # Test cellClicked signals
        self.assertIsNotNone(
            self.controller._view.left_board_and_player.board.cellClicked)
        self.assertIsNotNone(
            self.controller._view.right_board_and_player.board.cellClicked)

        # Test game_over_dialog signals
        self.assertIsNotNone(
            self.controller._view.game_over_dialog.back_menu_button)
        self.assertIsNotNone(
            self.controller._view.game_over_dialog.back_menu_button.clicked)

    def test_update(self):
        self.assertIsNone(self.view.game_over_dialog.get_name_winner())

        self.model.move_player.ships = []
        self.model.check_game_over()

        self.controller.update()

        self.assertEqual(
            self.view.game_over_dialog.get_name_winner(),
            self.model.move_player.name)
        self.assertEqual(self.view.game_over_dialog.isVisible(), True)
        self.assertEqual(self.controller._timer.isActive(), False)

    def test_update_view(self):
        # Mock methods
        self.controller.update_parts_view = MagicMock()
        self.controller.update_move_player_view = MagicMock()
        self.controller.update_board_view = MagicMock()

        self.controller.update_view()

        self.controller.update_parts_view.assert_called_once()
        self.controller.update_move_player_view.assert_called_once()
        self.controller.update_board_view.assert_called_once()

    def test_update_time(self):
        self.model.move_player.time = 10
        self.controller.update = MagicMock()

        self.controller.update_time()

        self.assertEqual(self.model.move_player.time, 9)
        self.assertEqual(
            self.controller._game_parts[self.model.move_player]
            .time_edit.time(), QTime(0, 0, 9))
        self.controller.update.assert_called_once()

    def test_update_parts_view(self):
        self.controller._game_parts[self.model.move_player]\
            .setEnabled = MagicMock()
        self.controller._game_parts[self.model.sleep_player]\
            .setEnabled = MagicMock()

        self.controller.update_parts_view()

        self.controller._game_parts[self.model.move_player]\
            .setEnabled.assert_called_once_with(True)
        self.controller._game_parts[self.model.sleep_player]\
            .setEnabled.assert_called_once_with(False)

    def test_update_move_player_view(self):
        self.controller._game_parts[self.model.move_player]\
            .move_player.setText = MagicMock()
        self.controller._game_parts[self.model.sleep_player]\
            .move_player.setText = MagicMock()

        self.controller.update_move_player_view()

        self.controller._game_parts[self.model.move_player]\
            .move_player.setText.assert_called_once_with(
            self.model.move_player.name)
        self.controller._game_parts[self.model.sleep_player]\
            .move_player.setText.assert_called_once_with('')

    def test_update_board_view(self):
        self.controller.get_code_board = MagicMock(
            side_effect=[[[0, 0], [0, 0]], [[0, 0], [0, 0]]])
        self.controller._game_parts[self.model.move_player]\
            .board.update_ = MagicMock()
        self.controller._game_parts[self.model.sleep_player]\
            .board.update_ = MagicMock()

        self.controller.update_board_view()

        self.controller.get_code_board.assert_has_calls([
            call(self.model.move_player.opponent_board),
            call(self.model.sleep_player.opponent_board)
        ])
        self.controller._game_parts[self.model.move_player]\
            .board.update_.assert_called_once_with([[0, 0], [0, 0]])
        self.controller._game_parts[self.model.sleep_player]\
            .board.update_.assert_called_once_with([[0, 0], [0, 0]])

    def test_get_code_board(self):
        cell_with_ship1 = CellWithShip(Ship((0, 1), 1, 1))
        ship = Ship((1, 0), 1, 1)
        cell_with_ship2 = CellWithShip(ship)
        cell_with_ship2.set_hit(True)
        cell = Cell()
        cell.set_hit(True)
        board = [
            [Cell(), cell_with_ship1],
            [cell_with_ship2, cell]
        ]

        code_board = self.controller.get_code_board(board)

        self.assertEqual(code_board, [[0, 3], [2, 1]])

    def test_choose_pos(self):
        self.controller.update = MagicMock()
        self.model.make_move = MagicMock()

        self.controller.choose_pos((0, 0))

        self.model.make_move.assert_called_once_with((0, 0))
        self.controller.update.assert_called_once()

    def test_set_game_over_action(self):
        action = MagicMock()

        self.controller.set_game_over_action(action)

        self.assertEqual(self.controller._game_over_action, action)


class PlacementShipsControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

        self.player = Player((10, 10), "Player1")
        self.available_ships = [(1, 2), (2, 3), (3, 4)]
        self.view = PlacementShipsView()
        self.controller = PlacementShipsController(
            self.player, self.available_ships, self.view)

    def tearDown(self):
        self.app.quit()
        self.app.deleteLater()

    def test_update_ready_status(self):
        self.controller.update_ready_status()
        self.assertFalse(self.view.ready_button.isEnabled())

        self.controller._available_ships = []
        self.controller.update_ready_status()
        self.assertTrue(self.view.ready_button.isEnabled())

    def test_update_available_ships_view(self):
        self.controller.update_available_ships_view()
        self.assertEqual(
            self.view.available_ships.table_ships.rowCount(),
            len(self.available_ships)
        )

    def test_update_board_view(self):
        self.controller.update_board_view()
        board = self.view.placement_management.board
        for row in range(self.player.height_board):
            for col in range(self.player.width_board):
                item = board.itemAt(row, col)
                cell_value = self.player.board[row][col]
                if isinstance(cell_value, CellWithShip):
                    if cell_value.get_ship() == self.controller._chose_ship:
                        self.assertEqual(
                            item.background().color().name(), "#ff0000")
                    else:
                        self.assertEqual(
                            item.background().color().name(), "#00ff00")
                else:
                    self.assertEqual(
                        item.background().color().name(), "#ffffff")

    def test_choose_size_ship(self):
        pos = (0, 0)
        self.controller.choose_size_ship(pos)
        chosen_ship = self.controller._chose_size_ship
        self.assertEqual(chosen_ship, self.available_ships[0])

    def test_choose_pos(self):
        pos = (0, 0)
        self.controller.choose_pos(pos)
        chosen_pos = self.controller._chose_pos
        chosen_ship = self.controller._chose_ship
        self.assertEqual(chosen_pos, pos)
        self.assertEqual(chosen_ship, self.player.get_ship(pos))

        # Test with chosen size ship
        size_ship = (1, 2)
        self.controller.choose_size_ship((0, 0))
        self.controller.choose_pos(pos)
        chosen_ship = self.controller._chose_ship
        self.assertIsNotNone(chosen_ship)
        self.assertEqual(chosen_ship.width, size_ship[0])
        self.assertEqual(chosen_ship.length, size_ship[1])

    def test_place_ship(self):
        pos = (0, 0)
        size_ship = (1, 2)
        self.controller.choose_size_ship((0, 0))
        self.controller.choose_pos(pos)
        self.controller.place_ship(size_ship)
        chosen_ship = self.controller._chose_ship
        self.assertIsNotNone(chosen_ship)
        self.assertEqual(chosen_ship.width, size_ship[0])
        self.assertEqual(chosen_ship.length, size_ship[1])
        self.assertNotIn(size_ship, self.available_ships)

    def test_remove_click(self):
        pos = (0, 0)
        size_ship = (1, 2)
        self.controller.choose_size_ship((0, 0))
        self.controller.choose_pos(pos)
        self.controller.place_ship(size_ship)

        self.controller.remove_click()
        chosen_ship = self.controller._chose_ship
        self.assertIsNone(chosen_ship)
        self.assertIn(size_ship, self.available_ships)

    def test_turn_click(self):
        pos = (0, 0)
        size_ship = (1, 2)
        self.controller.choose_size_ship((0, 0))
        self.controller.choose_pos(pos)
        self.controller.place_ship(size_ship)

        self.controller.turn_click()
        chosen_ship = self.controller._chose_ship
        self.assertIsNotNone(chosen_ship)
        self.assertEqual(chosen_ship.width, size_ship[0])
        self.assertEqual(chosen_ship.length, size_ship[1])

    def test_random_click(self):
        self.controller.random_click()
        self.assertEqual(len(self.controller._available_ships), 0)

    def test_ready_click(self):
        self.view.name_input.input.setText("New Name")
        self.controller.ready_click()
        self.assertEqual(self.player.name, "New Name")

    def test_set_ready_action(self):
        def ready_action():
            print("Ready action called")
        self.controller.set_ready_action(ready_action)
        self.assertEqual(self.controller._ready_action, ready_action)

    def test_set_player(self):
        new_player = Player((8, 8), "Player2")
        self.controller.set_player(new_player)
        self.assertEqual(self.controller._player, new_player)

    def test_set_available_ships(self):
        new_ships = [(1, 2), (3, 4)]
        self.controller.set_available_ships(new_ships)
        self.assertEqual(self.controller._available_ships, new_ships)


class SettingsControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.model = SettingsModel()
        self.view = SettingsMenuView()
        self.controller = SettingsController(self.model, self.view)

    def tearDown(self):
        self.app.quit()
        self.app.deleteLater()

    def test_setup_ships_view(self):
        ships = [(1, 4), (2, 3), (3, 2)]
        self.model.set_ships(ships)
        self.controller._setup_ships_view()
        table_ships = self.view.settings.table_ships
        self.assertEqual(table_ships.get_list_ships(), ships)

    def test_setup_board_size_view(self):
        board_size = (10, 10)
        self.model.set_board_size(board_size)
        self.controller._setup_board_size_view()
        self.assertEqual(self.view.settings.get_board_size(), board_size)

    def test_setup_bot_levels_view(self):
        self.model.set_bot_level(BotDifficulty.EASY)
        self.controller._setup_bot_levels_view()
        self.assertEqual(self.view.settings.bot_levels_box.currentIndex(), 0)

        self.model.set_bot_level(BotDifficulty.SMART)
        self.controller._setup_bot_levels_view()
        self.assertEqual(self.view.settings.bot_levels_box.currentIndex(), 1)

    def test_save_board_size(self):
        board_size = (12, 12)
        self.view.settings.set_board_size(board_size)
        self.controller._save_board_size()
        self.assertEqual(self.model.get_board_size(), board_size)

    def test_save_ships(self):
        ships = [(1, 4), (2, 3), (3, 2)]
        self.view.settings.table_ships.set_ships(ships)
        self.controller._save_ships()
        self.assertEqual(self.model.get_ships(), ships)

    def test_save_bot_level(self):
        self.view.settings.bot_levels_box.setCurrentIndex(0)
        self.controller._save_bot_level()
        self.assertEqual(self.model.get_bot_level(), BotDifficulty.EASY)

        self.view.settings.bot_levels_box.setCurrentIndex(1)
        self.controller._save_bot_level()
        self.assertEqual(self.model.get_bot_level(), BotDifficulty.SMART)

    def test_save_exit_buttons_view(self):
        save_and_exit_button = self.view.save_exit_buttons\
            .save_and_exit_button
        exit_button = self.view.save_exit_buttons.exit_button

        save_and_exit_button.click()
        self.assertIsNone(self.controller._exit_action)

        exit_button.click()
        self.assertIsNone(self.controller._exit_action)

    def test_set_exit_action(self):
        action_called = False

        def test_action():
            nonlocal action_called
            action_called = True

        self.controller.set_exit_action(test_action)
        self.controller._exit()
        self.assertTrue(action_called)


if __name__ == '__main__':
    unittest.main()
