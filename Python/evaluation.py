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
    def eval_12(awale, player):
        t = awale.board[player * 6:(1 + player) * 6]
        somme = 0
        for k in range(6):
            if t[k] == 1 or t[k] == 2:
                somme += t[k]
        return somme / 12

    @staticmethod
    def eval_krou(awale, player):
        t = awale.board[player * 6: (1 + player) * 6]
        maxi = 0
        for k in range(6):
            if 11 - k <= t[k] <= 33 - k:  # teste si c'est un krou
                maxi = t[k]
        if maxi == 0:
            return 0
        else:
            return 1

    @staticmethod
    def evaluation2(awale, player):
        w = [-0.4, 0.4, 0.1, -0.1]
        entier = awale.score[player] - awale.score[1 - player]
        allier_12 = Evaluation.eval_12(awale, player)  # nombre total de 1-2 chez nous (mauvais)
        adversaire_12 = Evaluation.eval_12(awale, 1 - player)  # nombre total de 1-2 chez l'autre (bon)
        allier_krou = Evaluation.eval_krou(awale, player)  # présence d'un krou sur notre terrain (bon)
        adversaire_krou = Evaluation.eval_krou(awale, 1 - player)  # présence d'un krou chez l'aversaire (mauvais)
        rep = entier + 0.5 + (w[0] * allier_12) + (w[1] * adversaire_12) + (w[3] * allier_krou) + (
            w[3] * adversaire_krou)
        rep = ((1000 * rep) // 1) / 1000
        return rep
