import pygame

from game.components.bot import Bot
from game.components.player import Player
from game.components.ship import Ship
from game.settings import Settings
from gui.displays.game_one_player_display import GameOnePlayerDisplay
from gui.displays.game_over_display import GameOverDisplay
from gui.displays.game_two_players_display import GameTwoPlayersDisplay
from gui.displays.main_menu_display import MainMenuDisplay
from game.logic import GameLogic


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sea Battle")
        self.window = pygame.display.set_mode((800, 400))
        self.main_menu = MainMenuDisplay(self.window.get_size())
        self.main_menu.play_vs_bot_button.set_action(self.play_vs_bot)
        self.main_menu.play_vs_player_button.set_action(self.play_vs_player)
        self.display = self.main_menu
        self.running = False
        self.game_logic = None

    def play_vs_bot(self):
        player = Player(board_size=Settings.board_size)
        ships = [Ship(1, 1),
                 Ship(1, 1),
                 Ship(1, 1),
                 Ship(1, 1),
                 Ship(1, 3),
                 Ship(1, 3),
                 Ship(1, 2),
                 Ship(2, 3),
                 Ship(1, 4)]
        player.place_ships_randomly(ships)
        # player.place_ship(Ship(1, 3), 7, 0, True)
        bot = Bot(board_size=Settings.board_size)
        bot.place_ship(Ship(1, 1), 0, 0)
        self.game_logic = GameLogic(player, bot)
        self.game_logic.start()
        self.display = GameOnePlayerDisplay(self.window.get_size(),
                                            self.game_logic)
        self.display.set_game_over_action(self.game_over)
        print('play vs bot')

    def back_to_menu(self):
        self.display = self.main_menu

    def game_over(self, name_winner):
        self.display = GameOverDisplay(self.window.get_size(), name_winner)
        self.display.back_to_menu_button.set_action(self.back_to_menu)

    def play_vs_player(self):
        player = Player(name="Player1")
        # player.place_ship(Ship(10, 10), 0, 0)
        player.place_ship(Ship(1, 3), 0, 0)
        bot = Player(name="Player2")
        bot.place_ship(Ship(1, 2), 0, 0, True)
        self.game_logic = GameLogic(player, bot)
        self.game_logic.start()
        self.display = GameTwoPlayersDisplay(self.window.get_size(),
                                             self.game_logic)
        self.display.set_game_over_action(self.game_over)
        print('play vs player')

    def start(self):
        self.running = True
        self.run()

    def stop(self):
        if self.game_logic:
            self.game_logic.stop()
        self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                else:
                    self.display.handle_event(event)
            self.display.render(self.window)
            pygame.display.flip()
