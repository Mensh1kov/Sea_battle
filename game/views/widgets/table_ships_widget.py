from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem
from pyqt5_plugins.examplebutton import QtWidgets


class TableShipsWidget(QTableWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(0, 2, widget)

        self.horizontalHeader().setDefaultSectionSize(119)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setDefaultSectionSize(23)
        self.verticalHeader().setMinimumSectionSize(0)
        self.setHorizontalHeaderLabels(['Width', 'Length'])

    def get_list_ships(self) -> list[(int, int)]:
        ships = []
        for row in range(self.rowCount()):
            ships.append(self.get_ship(row))
        return ships

    def get_ship(self, row: int) -> (int, int):
        if row < self.rowCount():
            row_data = []
            for column in range(self.columnCount()):
                row_data.append(int(self.item(row, column).text()))
            return tuple(row_data)

    def add_ship(self):
        self.insertRow(0)

    def remove_ship(self):
        self.removeRow(self.rowCount() - 1)

    def set_ships(self, ships: list[(int, int)]):
        self.setRowCount(0)
        for row in range(len(ships)):
            self.insertRow(row)
            for column, value in enumerate(ships[row]):
                self.setItem(row, column, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    game_part = TableShipsWidget()
    game_part.set_ships([(1, 2), (2, 3)])
    game_part.show()
    sys.exit(app.exec_())
