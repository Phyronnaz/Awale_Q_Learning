import random


class RandomPlayer:
    @staticmethod
    def get_move(awale, player):
        """
        :param awale: jeu d'awalé
        :param player: numéro du joueur
        :return: indice de la case choisie par le joueur
        """
        minmove = player * 6
        maxmove = (1 + player) * 6
        can_play = False

        while not can_play:
            move = random.randint(minmove, maxmove)
            can_play = awale.can_play(player, move)

        return move
