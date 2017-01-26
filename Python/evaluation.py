#  TODO : classe ?


class Evaluation:
    @staticmethod
    def evaluation1(awale, player):
        """
        :param awale: plateau actuel de la partie
        :param player: numéro du joueur
        :return: valeur numérique de l'état actuel de la partie
        """
        return awale.score[player] - awale.score[1 - player]

    @staticmethod
    def eval_1_2(awale, player):
        """
        :param awale: plateau actuel de la partie
        :param player: numéro du joueur
        :return: valeur numérique de la qualité territoire du joueur selon le nombre de trous à 1 ou 2 graines
        """
        minmove = 6 * player
        maxmove = 6 * (1 + player)
        s = 0

        for i in range(minmove, maxmove):
            if awale.board[i] == 1 or awale.board[i] == 2:
                s += awale.board[i]

        return s / 12

    @staticmethod
    def eval_krou(awale, player):
        """
        :param awale: plateau actuel de la partien
        :param player: numéro du joueur
        :return: nombre de krous sur le territoire du joueur
        """
        minmove = 6 * player
        maxmove = 6 * (1 + player)
        krou = False
        i = minmove

        while not krou and i < maxmove:
            if 11 - i <= awale.board[i] <= 33 - i:
                krou = True

        return int(krou)

    @staticmethod
    def evaluation2(awale, player):
        w = [0.4, 0.1]
        score = awale.score[player] - awale.score[1 - player]
        player_1_2 = Evaluation.eval_1_2(awale, player)  # nombre total de 1-2 chez nous (mauvais)
        opponent_1_2 = Evaluation.eval_1_2(awale, 1 - player)  # nombre total de 1-2 chez l'autre (bon)
        player_krou = Evaluation.eval_krou(awale, player)  # présence d'un krou sur notre terrain (bon)
        opponent_krou = Evaluation.eval_krou(awale, 1 - player)  # présence d'un krou chez l'aversaire (mauvais)
        rep = score + 0.5 + (w[0] * opponent_1_2) + (w[1] * player_krou) - (w[0] * player_1_2) - (w[1] * opponent_krou)
        return rep
