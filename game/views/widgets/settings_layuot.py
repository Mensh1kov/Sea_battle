from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, \
    QSpinBox, QPushButton, QComboBox

from game.views.widgets.my_label import MyLabel
from game.views.widgets.table_ships_widget import TableShipsWidget


class BotLevelsBox(QComboBox):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.addItems(['Easy', 'Smart'])


class SettingsWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.setFixedSize(261, 301)

        self.board_with_spin = QSpinBox(self)
        self.board_with_spin.setMinimum(5)
        self.board_with_spin.setMaximum(25)
        self.board_height_spin = QSpinBox(self)
        self.board_height_spin.setMinimum(5)
        self.board_height_spin.setMaximum(25)
        self.table_ships = TableShipsWidget(self)
        self.add_ship_button = QPushButton('Add', self)
        self.remove_ship_button = QPushButton('Remove', self)
        self.bot_levels_box = BotLevelsBox(self)
        self.layout = QGridLayout(self)

        self._setup_layout()
        self._setup_logic()

    def _setup_layout(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(MyLabel(15, 'Bot level', self), 0, 0, 1, 6)
        self.layout.addWidget(self.bot_levels_box, 1, 2, 1, 2)
        self.layout.addWidget(MyLabel(15, 'Board size', self), 2, 0, 1, 6)
        self.layout.addWidget(MyLabel(10, 'Width', self), 3, 0, 1, 2)
        self.layout.addWidget(self.board_with_spin)
        self.layout.addWidget(MyLabel(10, 'Height', self), 3, 3, 1, 2)
        self.layout.addWidget(self.board_height_spin)
        self.layout.addWidget(MyLabel(15, 'Ships', self), 4, 0, 1, 6)
        self.layout.addWidget(self.table_ships, 5, 0, 1, 6)
        self.layout.addWidget(self.add_ship_button, 6, 0, 1, 3)
        self.layout.addWidget(self.remove_ship_button, 6, 3, 1, 3)

    def _setup_logic(self):
        table = self.table_ships
        self.add_ship_button.clicked.connect(table.add_ship)
        self.remove_ship_button.clicked.connect(table.removeRow)

    def set_board_size(self, size: (int, int)):
        self.board_with_spin.setValue(size[0])
        self.board_height_spin.setValue(size[1])

    def get_board_size(self) -> (int, int):
        return (int(self.board_with_spin.text()),
                int(self.board_height_spin.text()))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    game_part = SettingsWidget()
    game_part.show()
    sys.exit(app.exec_())
