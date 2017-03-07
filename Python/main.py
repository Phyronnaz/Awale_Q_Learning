import numpy


# TODO : Revoir la documentation des fonctions.
def init_board():
    """
    Le plateau de jeu est constitué de 2 rangées de 6 trous, chaque trou contenant 4 graines au départ par défaut.
    Le score de chaque joueur est initalisé à 0 par défaut.
    """
    board = 4 * numpy.ones(12, numpy.int)
    # Vaut -2 tant que la partie n'est pas finie, -1 s'il y a égalité et le numéro du joueur s'il y a un gagnant.

    return board


def deal(board, move):
    """
    Distribue les graines de la case indiquée et renvoie le nouveau plateau ainsi que l'indice de la case d'arrivée.
    :param move: indice de la case à jouer
    :return: nouveau plateau, case d'arrivée
    """
    assert min(board) >= 0

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


def pick(board, score, player, move):
    """
    Ramasse les graines et renvoie le nouveau plateau ainsi que le nouveau score.
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: nouveau plateau, nouveau score
    """
    new_board, i = deal(board, move)
    new_score = score[:]
    minpick = (1 - player) * 6
    maxpick = (2 - player) * 6

    while minpick <= i < maxpick and 2 <= new_board[i] <= 3:
        new_score[player] += new_board[i]
        new_board[i] = 0
        i -= 1

    return new_board, new_score


def will_starve(board, score, player, move):
    """
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: "va affamer l'adversaire"
    """
    minpick = (1 - player) * 6
    maxpick = (2 - player) * 6
    new_board = pick(board, score, player, move)[0]
    starving = new_board[minpick:maxpick].sum() == 0

    return starving


def cannot_feed(board, score, player):
    """
    :param player: numéro du joueur
    :return: "ne peut pas nourrir l'adversaire"
    """
    minmove = player * 6
    maxmove = (1 + player) * 6
    cannot_feed = True

    for i in range(minmove, maxmove):
        cannot_feed = cannot_feed and will_starve(board, score, player, i)

    return cannot_feed


def can_play(board, score, player, move):
    """
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: "le coup est valide"
    """
    minmove = player * 6
    maxmove = (1 + player) * 6
    minpick = (1 - player) * 6
    maxpick = (2 - player) * 6

    if board[minpick:maxpick].sum() == 0:
        return minmove <= move < maxmove and board[move] != 0 and (
            not will_starve(board, score, player, move) or cannot_feed(board, score, player))
    else:
        return minmove <= move < maxmove and board[move] != 0


def play(board, score, player, move):
    """
    Joue le coup indiqué. Si le coup affame l'adversaire, le joueur ne ramasse pas les graines.
    :param player: numéro du joueur
    :param move: indice de la case à jouer
    :return: aucun retour
    """
    if will_starve(board, score, player, move):
        new_board = deal(board, move)[0]
        board = new_board
    else:
        board, score = pick(board, score, player, move)

    return board, score


def get_seeds(board, score):
    """
    Partage les graines s'il en reste sur le plateau à la fin de la partie : chaque joueur récupère les graines
    qui sont dans sa rangée.
    :return: aucun retour
    """
    for i in range(12):
        if board[i] != 0:
            score[i // 6] += board[i]
            board[i] = 0


def get_winner(board, score, winner, player):
    """
    Vérifie si la partie est terminée.
    :param player: numéro du joueur qui vient de jouer
    :return: aucun retour
    """
    if winner == -2:
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        if board[minpick:maxpick].sum() == 0 or score[player] >= 24:
            winner = player
        elif score[1 - player] >= 24:
            winner = 1 - player

    return winner

def pretty_print(board):
    north = board[6:12][::-1]
    south = board[0:6]

    print(numpy.array([north, south]))