from collections.abc import Callable
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from game.models.components.cell import CellWithShip
from game.models.components.player import Player
from game.models.components.ship import Ship
from game.views.placement_ships_view import PlacementShipsView


class PlacementShipsController:
    def __init__(self, player: Player,
                 available_ships: list[(int, int)],
                 view: PlacementShipsView):
        self._player = player
        self._view = view
        self._available_ships = available_ships
        self._ready_action = None
        self._chose_size_ship: (int, int) = None
        self._chose_pos: (int, int) = None
        self._chose_ship: Ship = None
        self.setup_view()

    def setup_view(self):
        self.setup_placement_management_view()
        self.setup_available_ships_view()
        self.setup_ready_view()
        self.setup_name_view()
        self.update_available_ships_view()
        self.update_board_view()
        self.update_ready_status()

    def setup_name_view(self):
        self._view.name_input.input.setText(self._player.name)

    def setup_ready_view(self):
        self._view.ready_button.clicked.connect(self.ready_click)

    def setup_placement_management_view(self):
        self._view.placement_management.random_button.clicked.connect(
            self.random_click)
        self._view.placement_management.turn_button.clicked.connect(
            self.turn_click)
        self._view.placement_management.remove_button.clicked.connect(
            self.remove_click)
        self._view.placement_management.board.cellClicked.connect(
            lambda *pos: self.choose_pos(pos))

    def setup_available_ships_view(self):
        self._view.available_ships.table_ships.cellClicked.connect(
            lambda *pos: self.choose_size_ship(pos))
        self._view.available_ships.table_ships.setEditTriggers(
            QAbstractItemView.NoEditTriggers)

    def update(self):
        self.update_available_ships_view()
        self.update_board_view()
        self.update_ready_status()

    def update_ready_status(self):
        self._view.ready_button.setEnabled(self.is_ready())

    def is_ready(self):
        return len(self._available_ships) == 0

    def update_available_ships_view(self):
        self._view.available_ships.table_ships.set_ships(
            self._available_ships)

    def update_board_view(self):
        code_board = []
        for row in self._player.board:
            code_row = []
            for cell in row:
                if isinstance(cell, CellWithShip):
                    if cell.get_ship() == self._chose_ship:
                        code_row.append(4)
                    else:
                        code_row.append(3)
                else:
                    code_row.append(0)
            code_board.append(code_row)
        self._view.placement_management.board.update_(code_board)

    def choose_size_ship(self, pos: (int, int)):
        self._chose_size_ship = self._view.available_ships.table_ships.\
            get_ship(pos[0])

    def choose_pos(self, pos: (int, int)):
        self._chose_pos = pos
        self.choose_ship(pos)
        if self._chose_size_ship:
            self.place_ship(self._chose_size_ship)
        else:
            self.update()

    def choose_ship(self, pos: (int, int)) -> Ship:
        self._chose_ship = self._player.get_ship(pos)

    def place_ship(self, size: (int, int)):
        ship = Ship(self._chose_pos, size[0], size[1])
        self._chose_ship = ship
        if self._player.place_ship(ship):
            self._available_ships.remove(self._chose_size_ship)
            self._chose_size_ship = None
            self.update()

    def remove_click(self):
        if self._chose_pos:
            if ship := self._player.remove_ship(self._chose_pos):
                self._available_ships.append((ship.width, ship.length))
                self.update()

    def turn_click(self):
        if self._chose_pos:
            if ship := self._player.remove_ship(self._chose_pos):
                ship.set_horizontal(not ship.horizontal)
                if not self._player.place_ship(ship):
                    self._available_ships.append((ship.width, ship.length))
                self.update()

    def random_click(self):
        self._player.place_ships_randomly(self._available_ships)
        self._available_ships = []
        self.update()

    def ready_click(self):
        if name := self._view.name_input.input.text():
            self._player.set_name(name)
        if self._ready_action:
            self._ready_action()

    def set_ready_action(self, action: Callable[(), None]):
        self._ready_action = action

    def set_player(self, player: Player):
        self._player = player
        self.setup_name_view()
        self.update()

    def set_available_ships(self, ships: list[(int, int)]):
        self._available_ships = ships
        self.update()


if __name__ == '__main__':
    app = QApplication([])
    player = Player()
    view = PlacementShipsView()
    controllers = PlacementShipsController(player, [(1, 1), (2, 1),
                                                    (3, 1), (5, 3)], view)
    view.show()
    app.exec_()
