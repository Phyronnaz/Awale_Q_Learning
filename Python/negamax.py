from awale import Awale


class Negamax:
    """
    créer l'arbre et renvoie le trou optimal à jouer
    """

    @staticmethod
    def negamax(awale, depth, player):
        if awale.winner != -2 or depth == 0:
            return awale.evaluation1(player)
        else:
            best_score = -float("inf")
            possible_move = []
            for i in range(6 * player, 6 * (1 + player)):
                if awale.can_play(player, i):
                    possible_move.append(i)
            if possible_move == [] and awale.board[(1 + player) * 6:(2 + player) * 6].sum() == 0:
                awale.winner = player
                # TODO: modifier la fonction, problème de la valeur retournée.
            best_move = possible_move[0]
            for j in possible_move:
                copy_awale = awale.copy()
                copy_awale.play(player, j)
                copy_awale.check_winner(player)
                new_awale = Awale(copy_awale.board, copy_awale.score, winner=copy_awale.winner)
                score = -Negamax.negamax(new_awale, depth - 1, 1 - player)
                if score >= best_score:
                    best_score = score
                    best_move = j
        return best_move
