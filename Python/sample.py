import numpy
from awale import Awale
from game import Game
from random_player import RandomPlayer
from negabeta_player import NegabetaPlayer
from evaluation import *

game = Game(RandomPlayer(), RandomPlayer())
sample = numpy.array([])

for k in range(10):
    print(k)
    game.awale = Awale()
    game.moves_count = 0
    player = 0

    while game.awale.winner == -2 and game.moves_count < game.max_count:
        game.moves_count += 1
        board = game.awale.board
        best_move = NegabetaPlayer(10, evaluation2).get_move(game.awale, player)
        numpy.append(sample, (board, best_move))
        move = game.players[player].get_move(game.awale, player)
        if game.awale.can_play(player, move):
            game.awale.play(player, move)
            game.awale.check_winner(player)
        else:
            raise Exception("Erreur! La case {} ne peut pas être jouée.".format(move))
        player = 1 - player
