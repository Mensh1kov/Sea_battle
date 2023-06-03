from typing import Union
from game.models.components.player import Player, ResultAttack


class GameModel:
    def __init__(self, player1: Player, player2: Player):
        self.move_player = player1
        self.sleep_player = player2
        self.winner = None

    def check_game_over(self):
        if self.is_game_over():
            if self.sleep_player.is_loser():
                self.winner = self.move_player
            else:
                self.winner = self.sleep_player

    def update(self, pos: (int, int), result: ResultAttack):
        self.move_player.update_opponent_board(*pos, result=result)
        self.check_game_over()

        if result not in (ResultAttack.HIT, ResultAttack.SUNK,
                          ResultAttack.ATTACKED):
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
