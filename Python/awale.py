import numpy


class Awale:
    """
    Le plateau de jeu est constitué de 2 rangées de 6 trous, contenant 4 graines au départ.
    On initialise le score de chaque joueur à 0.
    """

    def __init__(self, board=None, score=None):
        self.board = board if board is not None else 4 * numpy.ones(12, numpy.int)
        self.score = score if score is not None else numpy.array([0, 0])

    def copy(self):
        """
        :return: copie de l'awalé
        """
        return Awale(numpy.copy(self.board), numpy.copy(self.score))

    def deal(self, move):
        """
        Distribue les graines de la case indiquée et renvoie le nouveau plateau ainsi que l'indice de la case d'arrivée.
        :param move: indice de la case à jouer
        :return: nouveau plateau, case d'arrivée
        """
        new_board = numpy.copy(self.board)
        seeds = new_board[move]
        new_board[move] = 0
        i = move
        while seeds > 0:
            i += 1
            if i % 12 != move:
                new_board[i % 12] += 1
                seeds -= 1
        return new_board, i % 12

    def pick(self, player, move):
        """
        Ramasse les graines et renvoie le nouveau plateau ainsi que le nouveau score.
        :param player: numéro du joueur
        :param move: indice de la case de la dernière graine posée
        :return: nouveau plateau, nouveau score
        """
        new_board, i = self.deal(move)
        new_score = numpy.copy(self.score)
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        while minpick <= i < maxpick and 2 <= new_board[i] <= 3:
            new_score[player] += new_board[i]
            new_board[i] = 0
            i -= 1
        return new_board, new_score

    def can_feed(self, player):
        """
        Compte le nombre de coups possibles pour le joueur, vérifie qu'il ne va pas affamer son adversaire.
        :param player: numéro du joueur
        :return: "un seul coup possible", "n'affame pas son adversaire"
        """
        feed = False
        minmove = player * 6
        maxmove = (1 + player) * 6
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        moves_count = 0
        for i in range(minmove, maxmove):
            if self.board[i] != 0:
                moves_count += 1
                feed = feed or self.pick(player, i)[0][minpick:maxpick].any() != 0
        return moves_count == 1, feed

    def can_play(self, player, move):
        """
        Vérifie que le coup indiqué est valide.
        :param player: numéro du joueur
        :param move: indice de la case à jouer
        :return: booléen "le coup est valide"
        """
        minmove = player * 6
        maxmove = (1 + player) * 6
        if minmove <= move < maxmove:
            minpick = (1 - player) * 6
            maxpick = (2 - player) * 6
            new_board = self.pick(player, move)[0]
            return self.board[move] != 0 and new_board[minpick:maxpick].any() != 0
        else:
            return False

    def eval1(self, player):
        """
        Affecte une valeur numérique à l'état actuel de la partie.
        :param player: numéro du joueur
        :return: évaluation de l'état acutel de la partie
        """
        return self.score[player] - self.score[1 - player]
