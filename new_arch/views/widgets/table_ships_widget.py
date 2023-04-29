from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem
from pyqt5_plugins.examplebutton import QtWidgets


class TableShipsWidget(QTableWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(0, 3, widget)

        self.horizontalHeader().setDefaultSectionSize(80)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setDefaultSectionSize(23)
        self.verticalHeader().setMinimumSectionSize(0)
        self.setHorizontalHeaderLabels(['Width', 'Height', 'Count'])

    def get_list_ships(self) -> list:
        rows = []
        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                row_data.append(int(self.item(row, column).text()))
            rows.append(tuple(row_data))
        return rows

    def add_ship(self):
        self.insertRow(0)

    def remove_ship(self):
        self.removeRow(self.rowCount() - 1)

    def set_ships(self, ships: list[tuple[int, int, int]]):
        for row in range(len(ships)):
            self.insertRow(row)
            for column, value in enumerate(ships[row]):
                self.setItem(row, column, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    game_part = TableShipsWidget()
    game_part.show()
    sys.exit(app.exec_())
