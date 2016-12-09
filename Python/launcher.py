from game import Game
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer

game = Game(NewbiePlayer(), HumanPlayer(), debug=True)
game.new_game()
game.display_result()
