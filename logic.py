import threading

from SeaBattle.components import *


class GameLogic(threading.Thread):
    def __init__(self, player1: Player, player2: Player):
        super().__init__()
        self.move_player = player1
        self.sleep_player = player2
        self.running = False
        self.winner = None

    def switch_players(self):
        self.move_player, self.sleep_player = self.sleep_player, self.move_player

    def is_game_over(self) -> bool:
        return self.sleep_player.is_loser() or self.move_player.is_loser()

    def stop(self):
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            pos = self.move_player.get_move()
            if not pos:
                continue
            result = self.sleep_player.fire(*pos)
            print(result)
            self.move_player.update_opponent_board(*pos, result=result)

            if self.is_game_over():
                self.winner = self.move_player
                return

            if result == ResultAttack.MISS:
                self.switch_players()
