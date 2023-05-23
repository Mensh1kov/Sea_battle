from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from game.views.widgets.board_widget import BoardWidget


class BoardAndPlayerWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.resize(400, 500)

        self.board = BoardWidget(10, 10, self)
        self.board.move(20, 120)
        # self.board.setGeometry(QtCore.QRect(19, 120, 362, 362))

        self.move_player = QtWidgets.QLabel(self)
        self.move_player.setGeometry(QtCore.QRect(20, 40, 360, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.move_player.setFont(font)
        self.move_player.setAlignment(QtCore.Qt.AlignCenter)
        self.move_player.setText("Player")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    game_part = BoardAndPlayerWidget()
    game_part.show()
    sys.exit(app.exec_())