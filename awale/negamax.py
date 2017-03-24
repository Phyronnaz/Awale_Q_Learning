from awale.awale import Awale
from awale.main import *
from awale.evaluation import *


def get_move_negamax(board: numpy.ndarray, score, count, player: int, depth: int):
    alpha = -float("inf")
    beta = float("inf")
    evaluation = evaluation2
    return negabeta(Awale(board, score, count), depth, player, alpha, beta, evaluation)[1]


def negabeta(awale, depth, player, alpha, beta, evaluation):
    if awale.winner != -2 or depth == 0:

        return evaluation(awale, player), 6 * player

    else:
        best_score = -float("inf")
        possible_moves = []
        minmove = 6 * player
        maxmove = 6 * (1 + player)

        for i in range(minmove, maxmove):
            if awale.can_play(player, i):
                possible_moves.append(i)

        best_move = possible_moves[0]

        for i in possible_moves:
            copy_awale = awale.copy()
            copy_awale.play(player, i)
            copy_awale.check_winner(player)
            new_awale = copy_awale.copy()
            score = -negabeta(new_awale, depth - 1, 1 - player, -beta, -alpha, evaluation)[0]
            if score > best_score:
                best_score = score
                best_move = i
                if best_score >= alpha:
                    alpha = best_score
                    if alpha >= beta:
                        break

    return best_score, best_move
