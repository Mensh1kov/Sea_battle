from PyQt5.QtWidgets import QMainWindow, QApplication
from game.components.player import Player
from new_arch.controllers.game_controller import GameController
from new_arch.controllers.placement_ships_controller import PlacementShipsController
from new_arch.controllers.settings_controller import SettingsController
from new_arch.models.game_model import GameModel
from new_arch.models.settings_model import SettingsModel
from new_arch.views.game_view import GameView
from new_arch.views.main_menu_view import MainMenuWidget
from new_arch.views.placement_ships_view import PlacementShipsView
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
        menu.exit_button.clicked.connect(self.exit_)

    def one_player(self):
        print('one player')

    def two_player(self):
        player = Player(self._settings.get_board_size())
        player2 = Player(self._settings.get_board_size())
        self.placement_ships(player, player2)

    def placement_ships(self, player1: Player, player2: Player):
        self.main_menu_view = self.main_window.takeCentralWidget()
        view = PlacementShipsView()
        self.main_window.setCentralWidget(view)
        controller = PlacementShipsController(player1,
                                              self._settings.get_ships(),
                                              view)
        def f():  # нужно еще подумать
            controller.set_player(player2)
            controller.set_available_ships(self._settings.get_ships())
            controller.set_ready_action(lambda: self.start_game(player1,
                                                                player2))
        controller.set_ready_action(f)

    def exit_(self):
        sys.exit()  # возможно, это не совсем корректно

    def settings(self):
        view = SettingsMenuView()
        self.main_menu_view = self.main_window.takeCentralWidget()
        self.main_window.setCentralWidget(view)
        controller = SettingsController(self._settings, view)
        controller.set_exit_action(self.back_to_main_menu)

    def back_to_main_menu(self):
        self.main_window.setCentralWidget(self.main_menu_view)

    def start_game(self, player1, player2):
        view = GameView()
        self.main_window.setCentralWidget(view)
        model = GameModel(player1, player2)
        controller = GameController(model, view)
        controller.set_game_over_action(lambda: self.back_to_main_menu())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setFixedSize(800, 500)
    _ = MainController(main_window)
    main_window.show()
    sys.exit(app.exec_())
