from awale import Awale


class Negamax:
    """
    créer l'arbre et renvoie le trou optimal à jouer
    """

    @staticmethod
    def negamax(awale, depth, player, game_over):
        if game_over or depth == 0:
            return awale.evaluation1(player)
        else:
            best_score = -float("inf")
            possible_move = []
            for i in range(6 * player, 6 * (1 + player)):
                if awale.can_play(player, i):
                    possible_move.append(i)
            best_move = possible_move[0]
            for j in possible_move:
                new_board, new_score = awale.pick(player, j)
                new_awale = Awale(new_board, new_score)
                minmove = player * 6
                maxmove = (1 + player) * 6
                minpick = (1 - player) * 6
                maxpick = (2 - player) * 6
                cannot_feed = new_awale.board[minpick:maxpick].sum() == 0

                for i in range(minmove, maxmove):
                    cannot_feed = cannot_feed and new_awale.will_starve(player, i)

                game_state = new_awale.score[player] >= 24 or new_awale.score[1 - player] >= 24 or cannot_feed
                score = -Negamax.negamax(new_awale, depth - 1, 1 - player, game_state)
                if score >= best_score:
                    best_score = score
                    best_move = j
        return best_move
