from collections.abc import Callable

from PyQt5.QtWidgets import QApplication

from game.models.components.bot import BotDifficulty
from game.models.settings_model import SettingsModel
from game.views.settings_menu_view import SettingsMenuView


class SettingsController:
    def __init__(self, model: SettingsModel, view: SettingsMenuView):
        self._model = model
        self._view = view
        self._exit_action = None
        self._setup_view()

    def _setup_view(self):
        self._setup_bot_levels_view()
        self._setup_ships_view()
        self._setup_board_size_view()
        self._setup_save_exit_buttons_view()

    def _setup_ships_view(self):
        ships = self._model.get_ships()
        self._view.settings.table_ships.set_ships(ships)

    def _setup_board_size_view(self):
        self._view.settings.set_board_size(self._model.get_board_size())

    def _setup_save_exit_buttons_view(self):
        self._view.save_exit_buttons.save_and_exit_button.clicked.connect(
            lambda: self._save_exit())
        self._view.save_exit_buttons.exit_button.clicked.connect(
            lambda: self._exit())

    def _setup_bot_levels_view(self):
        if self._model.get_bot_level() == BotDifficulty.EASY:
            self._view.settings.bot_levels_box.setCurrentIndex(0)
        else:
            self._view.settings.bot_levels_box.setCurrentIndex(1)

    def _save_exit(self):
        self._save_board_size()
        self._save_ships()
        self._save_bot_level()
        self._exit()

    def _save_board_size(self):
        self._model.set_board_size(self._view.settings.get_board_size())

    def _save_ships(self):
        self._model.set_ships(
            self._view.settings.table_ships.get_list_ships())

    def _save_bot_level(self):
        if self._view.settings.bot_levels_box.currentIndex() == 0:
            self._model.set_bot_level(BotDifficulty.EASY)
        else:
            self._model.set_bot_level(BotDifficulty.SMART)

    def _exit(self):
        if self._exit_action:
            self._exit_action()

    def set_exit_action(self, action: Callable[(), None]):
        self._exit_action = action


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = SettingsModel()
    game_part = SettingsMenuView()
    c = SettingsController(m, game_part)
    game_part.show()
    sys.exit(app.exec_())
