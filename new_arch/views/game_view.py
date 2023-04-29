from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from new_arch.views.widgets.board_and_player_widget import BoardAndPlayerWidget
from new_arch.views.widgets.game_over_dialog import GameOverDialog


class GamePlayWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.resize(800, 500)

        self.game_over_dialog = GameOverDialog(self)
        self.left_board_and_player = BoardAndPlayerWidget(self)
        self.right_board_and_player = BoardAndPlayerWidget(self)
        self.right_board_and_player.move(400, 0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    game_part = GamePlayWidget()
    game_part.show()
    sys.exit(app.exec_())
