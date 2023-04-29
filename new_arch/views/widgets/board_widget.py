from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, \
    QSizePolicy, QVBoxLayout, QAbstractItemView


class BoardWidget(QTableWidget):
    def __init__(self, rows: int, columns: int, widget: QWidget = None):
        super().__init__(rows, columns, widget)
        self._size = 360
        self.setFixedSize(self._size, self._size)
        self._cell_width = self._size // columns
        self._cell_height = self._size // rows

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setMinimumSectionSize(5)
        self.verticalHeader().setMinimumSectionSize(5)
        self.horizontalHeader().setDefaultSectionSize(self._cell_width)
        self.verticalHeader().setDefaultSectionSize(self._cell_height)

        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.cellClicked.connect(lambda *args: print(args))


if __name__ == '__main__':
    app = QApplication([])
    window = BoardWidget(5, 5)
    window.show()
    app.exec_()
