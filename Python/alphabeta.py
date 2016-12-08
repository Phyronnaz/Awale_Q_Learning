from awale import Awale


class Alphabeta:
    @staticmethod
    def alphabeta(awale, depth, player, alpha, beta):

        if awale.winner != -2 or depth == 0:
            return [awale.evaluation1(player), 6 * player]
        else:
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
                new_awale = Awale(copy_awale.board, copy_awale.score, winner=copy_awale.winner)
                score = -Alphabeta.alphabeta(new_awale, depth-1, 1 - player, -beta, -alpha)[0]
                if score >= alpha:
                    alpha = score
                    best_move = i
                    if alpha >= beta:
                        break
        return [alpha, best_move]
