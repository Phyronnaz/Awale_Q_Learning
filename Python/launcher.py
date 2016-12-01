from game import Game
from human_player import HumanPlayer
from negamax_player import NegamaxPlayer


game = Game(NegamaxPlayer(), HumanPlayer())
game.new_game()
