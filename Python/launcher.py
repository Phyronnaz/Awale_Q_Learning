from game import Game
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from evaluation import Evaluation

game = Game(NegabetaPlayer(5 ,Evaluation.evaluation1), NegabetaPlayer(5, Evaluation.evaluation2), debug=False)
game.new_game()
game.display_result()
