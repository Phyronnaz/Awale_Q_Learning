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
        alpha = -0.4
        beta = 0.4
        gamma = 0.1
        delta = -0.1
        entier = awale.score[player] - awale.score[1 - player]
        plateau=awale.board
        allier_12 = Evaluation.eval_12(plateau, player)  # nombre total de 1-2 chez nous (mauvais)
        adversaire_12 = Evaluation.eval_12(plateau, 1 - player)  # nombre total de 1-2 chez l'autre (bon)
        allier_krou = Evaluation.eval_krou(plateau, player)  # présence d'un krou sur notre terrain (bon)
        adversaire_krou = Evaluation.eval_krou(plateau, 1 - player)  # présence d'un krou chez l'aversaire (mauvais)
        rep = entier + 0.5 + (alpha * allier_12) + (beta * adversaire_12) + (gamma * allier_krou) + (
            delta * adversaire_krou)
        rep = ((1000 * rep) // 1) / 1000
        return rep
