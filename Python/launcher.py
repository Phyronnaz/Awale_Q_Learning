from game import Game
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from alphabeta_player import AlphabetaPlayer

game = Game(NegamaxPlayer(4), NegamaxPlayer(6), debug=False)
game.new_game()
game.display_result()
