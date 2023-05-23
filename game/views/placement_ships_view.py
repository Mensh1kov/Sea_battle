from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from game.views.widgets.board_widget import BoardWidget
from game.views.widgets.my_button import MyButton
from game.views.widgets.my_label import MyLabel
from game.views.widgets.table_ships_widget import TableShipsWidget


class NameInputWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.addWidget(MyLabel(15, 'Name', self))
        self.input = QtWidgets.QLineEdit(self)
        self.input.setMinimumSize(QtCore.QSize(0, 20))
        self.input.setFont(QFont(None, 15))
        self._layout.addWidget(self.input)


class AvailableShipsWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addWidget(MyLabel(15, 'Ships', self))
        self.table_ships = TableShipsWidget(self)
        self._layout.addWidget(self.table_ships)


class PlacementManagementWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self._layout = QtWidgets.QGridLayout(self)
        self.turn_button = MyButton(40, 12, 'Turn', self)
        self._layout.addWidget(self.turn_button, 2, 1, 1, 1)
        self.board = BoardWidget(10, 10, self)
        self._layout.addWidget(self.board, 1, 0, 1, 2)

        self.random_button = MyButton(40, 12, 'Random', self)
        self._layout.addWidget(self.random_button, 0, 0, 1, 2)
        self.remove_button = MyButton(40, 12, 'Remove', self)
        self._layout.addWidget(self.remove_button, 2, 0, 1, 1)


class PlacementShipsView(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.setFixedSize(800, 500)
        self.name_input = NameInputWidget(self)
        self.name_input.move(500, 30)
        self.available_ships = AvailableShipsWidget(self)
        self.available_ships.move(500, 120)
        self.placement_management = PlacementManagementWidget(self)
        self.placement_management.move(30, 30)
        self.ready_button = MyButton(40, 12, 'Ready', self)
        self.ready_button.setGeometry(QtCore.QRect(500, 440, 270, 40))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = PlacementShipsView()
    Form.show()
    sys.exit(app.exec_())