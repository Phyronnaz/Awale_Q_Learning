# TODO: Comparer temps d'éxécution Negabeta/Negamax
# TODO: Nombre de coup
from game import Game
from awale.evaluation import *
from negabeta_player import NegabetaPlayer

rep = [[] for _ in range(10)]
for i in range(1, 11):
    for j in range(1, 11):
        game = Game(NegabetaPlayer(i, evaluation2), NegabetaPlayer(j, evaluation1), debug=False)
        game.new_game()
        rep[i - 1].append(game.awale.score)
    print(i)
print(rep)