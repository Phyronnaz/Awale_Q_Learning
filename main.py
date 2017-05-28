import numpy


def init_board():
    """
    Le plateau de jeu est constitué de 2 rangées de 6 trous, chaque trou contenant 4 graines au départ.
    """
    board = 4 * numpy.ones(12, numpy.int)

    return board


def deal(board, move):
    """
    Distribue les graines de la case indiquée et renvoie le nouveau plateau ainsi que l'indice de la case d'arrivée.
    :param board: plateau
    :param move: indice de la case à jouer
    :return: nouveau plateau, case d'arrivée
    """
    new_board = numpy.copy(board)
    seeds = new_board[move]
    new_board[move] = 0
    i = move

    while seeds > 0:
        i += 1
        if i % 12 != move:
            new_board[i % 12] += 1
            seeds -= 1

    return new_board, i % 12


def pick(board, move):
    """
    Ramasse les graines et renvoie le nouveau plateau ainsi que le nouveau score.
    :param board: plateau
    :param move: indice de la case à jouer
    :return: nouveau plateau, nouveau score
    """
    new_board, i = deal(board, move)
    score = 0
    minpick = 6
    maxpick = 12

    while minpick <= i < maxpick and 2 <= new_board[i] <= 3:
        score += new_board[i]
        new_board[i] = 0
        i -= 1

    return new_board, score


def will_starve(board, move):
    """
    Vérifie si le joueur va affamer l'adversaire.
    :param board: plateau
    :param move: indice de la case à jouer
    :return: "va affamer l'adversaire"
    """
    minpick = 6
    maxpick = 12
    new_board = pick(board, move)[0]
    starving = new_board[minpick:maxpick].sum() == 0

    return starving


def cannot_feed(board):
    """
    Vérifie si le joueur ne peut pas nourrir l'adversaire.
    :param board: plateau
    :return: "ne peut pas nourrir l'adversaire"
    """
    minmove = 0
    maxmove = 6
    cannot_feed = True

    for i in range(minmove, maxmove):
        cannot_feed = cannot_feed and will_starve(board, i)

    return cannot_feed


def can_play(board, move):
    """
    Vérifie si le coup indiqué est valide.
    :param board: plateau
    :param move: indice de la case à jouer
    :return: "le coup est valide"
    """
    minmove = 0
    maxmove = 6
    minpick = 6
    maxpick = 12

    if board[minpick:maxpick].sum() == 0:
        return minmove <= move < maxmove and board[move] != 0 and (not will_starve(board, move) or cannot_feed(board))
    else:
        return minmove <= move < maxmove and board[move] != 0


def play(board, move):
    """
    Joue le coup indiqué. Si le coup affame l'adversaire, le joueur ne ramasse pas les graines.
    :param move: indice de la case à jouer
    :return: aucun retour
    """
    if will_starve(board, move):
        new_board = deal(board, move)[0]
        board = new_board
        score = 0
    else:
        board, score = pick(board, move)

    return board, score


def get_seeds(board, scores):
    """
    Partage les graines s'il en reste sur le plateau à la fin de la partie : chaque joueur récupère les graines
    qui sont dans son territoire.
    :param board: plateau
    :param scores: score
    :return: aucun retour
    """
    for i in range(12):
        if board[i] != 0:
            scores[i // 6] += board[i]
            board[i] = 0


def get_winner(board, scores, winner, player):
    """
    Vérifie si la partie est terminée : winner vaut -2 si la partie n'est pas terminée, -1 s'il y a égalité ou le numéro
    du gagnant sinon.
    :param board: plateau
    :param scores: score
    :param winner: numéro du gagnant ou -2 si la partie n'est pas terminée
    :param player: numéro du joueur qui vient de jouer
    :return: nouvel état
    """
    if winner == -2:
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        if board[minpick:maxpick].sum() == 0 or scores[player] >= 24:
            winner = player
        elif scores[1 - player] >= 24:
            winner = 1 - player

    return winner


def invert_players(board):
    l = numpy.zeros(12, dtype=int)
    l1 = board[:6].copy()
    l2 = board[6:].copy()
    l[:6] = l2
    l[6:] = l1
    return l


def invert(board, player):
    return board.copy() if player == 0 else invert_players(board)
