from game import Game
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from alphabeta_player import AlphabetaPlayer


game = Game(AlphabetaPlayer(6),AlphabetaPlayer(2), debug=False)
game.new_game()
game.display_result()