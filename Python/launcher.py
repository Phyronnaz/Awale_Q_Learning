from game import Game
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer

game = Game(NewbiePlayer(), NegamaxPlayer(3), debug=False)
game.new_game()
game.display_result()