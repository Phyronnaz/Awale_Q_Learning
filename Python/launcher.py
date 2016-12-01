from game import Game
from human_player import HumanPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer

game = Game(HumanPlayer(), HumanPlayer())
game.new_game()
