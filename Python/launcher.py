from game import Game
from human_player import HumanPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer

game = Game(NegamaxPlayer(3), NegamaxPlayer(4))  #Bug pour une profondeur de 4 contre 5 et 5 contre 6
game.new_game()
print(game.display_result())
