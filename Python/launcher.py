from game import Game
from human_player import HumanPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer

game = Game(NegamaxPlayer(5), NegamaxPlayer(6))
game.new_game()
print(game.display_result())
