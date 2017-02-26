from awale import Awale


def negamax(awale, depth, player, evaluation):
    """
    Calcule le meilleur score et le meilleur coup possible.
    :param awale: jeu d'awalé
    :param depth: profondeur de l'arbre
    :param player: numéro du joueur
    :param evaluation: fonction d'évaluation du joueur
    :return: meilleur score, meilleur coup
    """
    if awale.winner != -2 or depth == 0:

        return evaluation(awale, player), 6 * player

    else:
        best_score = -float("inf")
        possible_moves = []
        minmove = player * 6
        maxmove = (1 + player) * 6

        for i in range(minmove, maxmove):
            if awale.can_play(player, i):
                possible_moves.append(i)

        best_move = possible_moves[0]

        for i in possible_moves:
            copy_awale = awale.copy()
            copy_awale.play(player, i)
            copy_awale.check_winner(player)
            new_awale = Awale(copy_awale.board, copy_awale.score, winner=copy_awale.winner)
            score = -negamax(new_awale, depth - 1, 1 - player, evaluation)[0]
            if score > best_score:
                best_score = score
                best_move = i

        return best_score, best_move
