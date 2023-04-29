from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, \
    QTableWidget, QTableWidgetItem, QAbstractItemView


class BoardWidget(QTableWidget):
    def __init__(self, rows: int, columns: int, widget: QWidget = None):
        super().__init__(rows, columns, widget)
        self._size = 360
        self.setFixedSize(self._size, self._size)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setMinimumSectionSize(5)
        self.verticalHeader().setMinimumSectionSize(5)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.setup_board(rows, columns)
        self.cellClicked.connect(lambda *args: print(args))

    def setup_board(self, rows: int, columns: int):
        cell_width = self._size // columns
        cell_height = self._size // rows
        self.horizontalHeader().setDefaultSectionSize(cell_width)
        self.verticalHeader().setDefaultSectionSize(cell_height)

    def pain_cell(self, row: int, column: int, color: (int, int, int)):
        item = QTableWidgetItem()
        item.setBackground(QColor(*color))
        self.setItem(row, column, item)

    def update_(self, board: list[list[int]]):
        rows = len(board)
        columns = len(board[0])
        self.setup_board(rows, columns)

        # Code:
        # 0 - empty
        # 1 - miss
        # 2 - hit
        # 3 - ship

        for row in range(rows):
            for column in range(columns):
                code = board[row][column]

                if code == 0:
                    pass
                elif code == 1:
                    self.pain_cell(row, column, (192, 192, 192))
                elif code == 2:
                    self.pain_cell(row, column, (255, 0, 0))
                else:
                    self.pain_cell(row, column, (64, 64, 64))


if __name__ == '__main__':
    app = QApplication([])
    window = BoardWidget(5, 5)
    window.update_([
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 2, 2, 0, 2],
        [0, 1, 1, 0, 2],
        [0, 3, 3, 0, 0]
    ])
    window.show()
    app.exec_()
