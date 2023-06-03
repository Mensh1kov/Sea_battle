from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication
from game.models.components.cell import CellWithShip
from game.models.components.player import Player
from game.models.components.ship import Ship
from game.models.game_model import GameModel
from game.views.game_view import GameView
from game.views.widgets.board_and_player_widget import BoardAndPlayerWidget


class GameController:
    def __init__(self, model: GameModel, view: GameView):
        self._model = model
        self._view = view
        self._game_parts: dict[Player, BoardAndPlayerWidget] = {}
        self._game_over_action = None
        self._timer = None
        self.setup()
        self.update()

    def setup(self):
        self.setup_controller()
        self.setup_view()
        self.setup_timer()

    def setup_timer(self):
        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.update_time)
        self._timer.start()

    def setup_controller(self):
        self._game_parts = {
            self._model.move_player: self._view.right_board_and_player,
            self._model.sleep_player: self._view.left_board_and_player
        }

    def setup_view(self):
        self._view.left_board_and_player.board.cellClicked.connect(
            lambda *pos: self.choose_pos(pos)
        )
        self._view.right_board_and_player.board.cellClicked.connect(
            lambda *pos: self.choose_pos(pos)
        )
        self._view.game_over_dialog.back_menu_button.clicked.connect(
            lambda: self._game_over_action()
        )
        m_player = self._model.move_player
        s_player = self._model.sleep_player
        self._game_parts[m_player].time_edit.setTime(
            QTime(0, 0, 0).addSecs(m_player.time)
        )
        self._game_parts[s_player].time_edit.setTime(
            QTime(0, 0, 0).addSecs(s_player.time)
        )

    def update(self):
        if winner := self._model.get_winner():
            self._view.game_over_dialog.set_name_winner(winner.name)
            self._view.game_over_dialog.show()
            self._timer.stop()
        self.update_view()

    def update_view(self):
        self.update_parts_view()
        self.update_move_player_view()
        self.update_board_view()

    def update_time(self):
        move_player = self._model.move_player
        move_player.time -= 1
        self._game_parts[move_player].time_edit.setTime(
            QTime(0, 0, 0).addSecs(move_player.time))
        self._model.check_game_over()
        self.update()

    def update_parts_view(self):
        self._game_parts.get(self._model.move_player).setEnabled(True)
        self._game_parts.get(self._model.sleep_player).setEnabled(False)

    def update_move_player_view(self):
        move_player = self._model.move_player
        self._game_parts.get(move_player).move_player.setText(
            move_player.name
        )
        self._game_parts.get(self._model.sleep_player).move_player.setText('')

    def update_board_view(self):
        move_player = self._model.move_player
        sleep_player = self._model.sleep_player
        self._game_parts.get(move_player).board.update_(
            self.get_code_board(move_player.opponent_board))
        self._game_parts.get(sleep_player).board.update_(
            self.get_code_board(sleep_player.opponent_board))

    def get_code_board(self, board: list[list]):
        code_board = []
        # Code:
        # 0 - empty
        # 1 - miss
        # 2 - hit
        # 3 - ship

        for row in board:
            code_row = []
            for cell in row:
                if isinstance(cell, CellWithShip):
                    if cell.is_hit():
                        code_row.append(2)
                    else:
                        code_row.append(3)
                elif cell.is_hit():
                    code_row.append(1)
                else:
                    code_row.append(0)
            code_board.append(code_row)
        return code_board

    def choose_pos(self, pos):
        self._model.make_move(pos)
        self.update()

    def set_game_over_action(self, action):
        self._game_over_action = action


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    player1 = Player((2, 2), '1')
    player1.place_ship(Ship((0, 0), 1, 1))
    player2 = Player((2, 2), '2')
    player2.place_ship(Ship((0, 0), 1, 2))
    model = GameModel(player1, player2)
    view = GameView()
    controller = GameController(model, view)
    view.show()
    sys.exit(app.exec_())