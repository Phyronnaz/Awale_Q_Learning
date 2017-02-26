import numpy
from awale import Awale
from game import Game
from random_player import RandomPlayer
from negabeta_player import NegabetaPlayer
from evaluation import *

game = Game(RandomPlayer(), RandomPlayer())
sample = [[], []]
target = [[], []]
for k in range(3):
    print(k)
    game.awale = Awale()
    game.moves_count = 0
    player = 0

    while game.awale.winner == -2 and game.moves_count < game.max_count:
        game.moves_count += 1
        best_move = NegabetaPlayer(10, evaluation2).get_move(game.awale, player)
        board = game.awale.board
        score = game.awale.score
        x = numpy.append(board, score)
        sample[player].append(x)
        target[player].append(best_move)
        move = game.players[player].get_move(game.awale, player)
        if game.awale.can_play(player, move):
            game.awale.play(player, move)
            game.awale.check_winner(player)
        else:
            raise Exception("Erreur! La case {} ne peut pas être jouée.".format(move))
        player = 1 - player

numpy.save('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\sample_player0', numpy.array(sample[0]))
numpy.save('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\target_player0', numpy.array(target[0]))
numpy.save('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\sample_player1', numpy.array(sample[1]))
numpy.save('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\target_player1', numpy.array(target[1]))

# TODO : justifier le choix de la profondeur de Negabeta, la méthode pour obtenir les plateaux et le nombre de plateaux.
