from game import Game
from human_player import HumanPlayer
from random_player import RandomPlayer
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from evaluation import Evaluation
import time

game = Game(NegabetaPlayer(6, Evaluation.evaluation2), NegabetaPlayer(7, Evaluation.evaluation2), debug=False)
t = time.clock()
game.new_game()
t = time.clock() - t
print(t / 60)
game.display_result()
