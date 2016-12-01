from game import Game
from human_player import HumanPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer

game = Game(NegamaxPlayer(4), NegamaxPlayer(5))  """ Bug pour une profondeur de 5 contre 6 et 4 contre 5, laisse des adversaires sans graines"""
game.new_game()
print(game.display_result())
