from copy import copy

from PyQt5.QtWidgets import QMainWindow, QApplication

from new_arch.controllers.settings_controller import SettingsController
from new_arch.models.settings_model import SettingsModel
from new_arch.views.main_menu_view import MainMenuWidget
from new_arch.views.settings_menu_view import SettingsMenuView


class MainController:
    def __init__(self, window: QMainWindow):
        self.main_window = window
        self.main_menu_view = MainMenuWidget()
        self.main_window.setCentralWidget(self.main_menu_view)
        self._settings = SettingsModel()

        self.setup_main_menu()

    def setup_main_menu(self):
        menu = self.main_menu_view
        menu.one_player_button.clicked.connect(self.one_player)
        menu.two_player_button.clicked.connect(self.two_player)
        menu.settings_button.clicked.connect(self.settings)
        menu.exit_button.clicked.connect(self.exit)

    def one_player(self):
        print('one player')

    def two_player(self):
        print('two player')

    def exit(self):
        print('exit')

    def settings(self):
        view = SettingsMenuView()
        self.main_menu_view = self.main_window.takeCentralWidget()
        self.main_window.setCentralWidget(view)
        controller = SettingsController(self._settings, view)
        controller.set_exit_action(self.back_to_main_menu)

    def back_to_main_menu(self):
        self.main_window.setCentralWidget(self.main_menu_view)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setFixedSize(800, 500)
    _ = MainController(main_window)
    main_window.show()
    sys.exit(app.exec_())
