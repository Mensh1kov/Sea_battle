from typing import Union
from game.components.player import Player, ResultAttack


class GameModel:
    def __init__(self, player1: Player, player2: Player):
        self.move_player = player1
        self.sleep_player = player2
        self.winner = None

    def update(self, pos: (int, int), result: ResultAttack):
        self.move_player.update_opponent_board(*pos, result=result)
        if self.is_game_over():
            self.winner = self.move_player

        if result not in (ResultAttack.HIT, ResultAttack.SUNK):
            self.switch_players()

    def make_move(self, pos: (int, int)):
        self.update(pos, self.sleep_player.fire(*pos))

    def switch_players(self):
        self.move_player, self.sleep_player = (self.sleep_player,
                                               self.move_player)

    def is_game_over(self) -> bool:
        return self.sleep_player.is_loser() or self.move_player.is_loser()

    def get_winner(self) -> Union[None, Player]:
        return self.winner
