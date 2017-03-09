#TODO: Faire de la profondeur 1 à 10 avec eval2 contre eval2, eval1 contre eval1, eval1 contre eval2 et eval2 contre eval1
#TODO: Comparer temps d'éxécution Negabeta/Negamax
#TODO: Nombre de coup
from game import Game
import numpy
from newbie_player import NewbiePlayer
from negamax_player import NegamaxPlayer
from negabeta_player import NegabetaPlayer
from evaluation import *

rep=[[] for _ in range(10)]
for i in range (1,11):
    for j in range (1,11):
        game = Game(NegabetaPlayer(i, evaluation1), NegabetaPlayer(j, evaluation1), debug=False)
        game.new_game()
        rep[i-1].append(game.awale.score)
    print(i)
print (rep)