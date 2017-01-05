import numpy


class Awale:
    """
    Permet de modéliser l'awalé.
    """

    def __init__(self, board=None, score=None, winner=-2):
        """
        Le plateau de jeu est constitué de 2 rangées de 6 trous, chaque trou contenant 4 graines au départ par défaut.
        Le score de chaque joueur est initalisé à 0 par défaut.
        :param board: plateu de jeu
        :param score: score des deux joueurs
        """
        self.board = board if board is not None else 4 * numpy.ones(12, numpy.int)
        self.score = score if score is not None else numpy.zeros(2, numpy.int)
        # Vaut -2 tant que la partie n'est pas finie, -1 s'il y a égalité et le numéro du joueur s'il y a un gagnant.
        self.winner = winner

    def copy(self):
        """
        :return: copie de l'awalé
        """
        board, score = numpy.copy(self.board), numpy.copy(self.score)

        return Awale(board, score, winner=self.winner)

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
        :param move: indice de la case à jouer
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

    def will_starve(self, player, move):
        """
        :param player: numéro du joueur
        :param move: indice de la case à jouer
        :return: "va affamer l'adversaire"
        """
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        new_board = self.pick(player, move)[0]
        starving = new_board[minpick:maxpick].sum() == 0

        return starving

    def cannot_feed(self, player):
        """
        :param player: numéro du joueur
        :return: "ne peut pas nourrir l'adversaire"
        """
        minmove = player * 6
        maxmove = (1 + player) * 6
        cannot_feed = True

        for i in range(minmove, maxmove):
            cannot_feed = cannot_feed and self.will_starve(player, i)

        return cannot_feed

    def can_play(self, player, move):
        """
        :param player: numéro du joueur
        :param move: indice de la case à jouer
        :return: "le coup est valide"
        """
        minmove = player * 6
        maxmove = (1 + player) * 6
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6

        if self.board[minpick:maxpick].sum() == 0:
            return minmove <= move < maxmove and self.board[move] != 0 and (
                not self.will_starve(player, move) or self.cannot_feed(player))
        else:
            return minmove <= move < maxmove and self.board[move] != 0

    def play(self, player, move):
        """
        Joue le coup indiqué. Si le coup affame l'adversaire, le joueur ne ramasse pas les graines.
        :param player: numéro du joueur
        :param move: indice de la case à jouer
        :return: aucun retour
        """
        if self.will_starve(player, move):
            new_board = self.deal(move)[0]
            self.board = new_board
        else:
            self.board, self.score = self.pick(player, move)

    def get_seeds(self):
        """
        Partage les graines s'il en reste sur le plateau à la fin de la partie : chaque joueur récupère les graines
        qui sont dans sa rangée.
        :return: aucun retour
        """
        for i in range(12):
            if self.board[i] != 0:
                self.score[i // 6] += self.board[i]
                self.board[i] = 0

    def check_winner(self, player):
        """
        Vérifie si la partie est terminée.
        :param player: numéro du joueur qui vient de jouer
        :return: aucun retour
        """
        if self.winner == -2:
            minpick = (1 - player) * 6
            maxpick = (2 - player) * 6
            if self.board[minpick:maxpick].sum() == 0 or self.score[player] >= 24:
                self.winner = player
            elif self.score[1 - player] >= 24:
                self.winner = 1 - player
