import numpy as np
from random import randint


class Awale:
    """
    Le plateau de jeu est constitué de 2 rangées de 6 trous, contenant 4 graines au départ.
    On initialise le score de chaque joueur à 0.
    """

    def __init__(self, board, score):
        self.board = board
        self.score = score
        self.game_over = False

    def copy(self):
        """
        :return: copie de l'awalé
        """
        return Awale(np.copy(self.board), self.score)

    def deal(self, move):
        """
        Distribue les graines de la case indiquée et renvoie le nouveau plateau ainsi que l'indice de la case d'arrivée.
        :param move: indice de la case à jouer
        :return: nouveau plateau, case d'arrivée
        """
        new_board = np.copy(self.board)
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
        new_score = np.copy(self.score)
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
        :return: booléen "un seul coup possible" et booléen "n'affame pas son adversaire"
        """
        feed = False
        minmove = player * 6
        maxmove = (1 + player) * 6
        minpick = (1 - player) * 6
        maxpick = (2 - player) * 6
        moves = 0
        for i in range(minmove, maxmove):
            moves += int(self.board[i] != 0)
            if self.board[i] != 0:
                feed = feed or self.pick(player, i)[0][minpick:maxpick].any() != 0
        return moves == 1, feed

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

    def play(self, player, move):
        """
        Joue le coup indiqué s'il est valide, oblige le joueur à choisir une autre case sinon et modifie le plateau
        ainsi que le score. Si le seul coup possible affame l'adversaire, le coup est joué sans ramasser les graines.
        :param player: numéro du joueur
        :param move: indice de la case à jouer
        :return: aucun retour
        """
        minmove = player * 6
        maxmove = (1 + player) * 6
        if self.can_feed(player)[0] and not(self.can_feed(player)[1]):
            while not(minmove <= move < maxmove) or self.board[move] == 0:
                    try:
                        move = int(input("Le coup est invalide, choisissez une autre case : "))
                    except ValueError:
                        move = -1
            self.board = self.deal(move)[0]
        else:
            while not self.can_play(player, move):
                try:
                    move = int(input("Le coup est invalide, choisissez une autre case : "))
                except ValueError:
                    move = -1
            self.board, self.score = self.pick(player, move)


def game():
    """
    Lance une partie d'awalé.
    :return: aucun retour
    """
    awale = Awale(4 * np.ones(12, np.int), [22, 0])
    player = 0
    print("Le joueur 0 est au sud : il doit jouer les cases de 0 à 5.\nLe joueur 1 est au nord : il doit jouer les"
          " cases de 6 à 11.\n")
    awale.game_over = awale.score[0] >= 24 or awale.score[1] >= 24 or (not awale.can_feed(player)[0] and
                                                                       not awale.can_feed(player)[1])
    while not awale.game_over:
        north = awale.board[6:12][::-1]
        south = awale.board[0:6]
        board = np.array([north, south])
        print(board)
        print("Score du joueur 0 :", awale.score[0], "\nScore du joueur 1 :", awale.score[1])
        print("\nC'est au joueur", player, "de jouer.")
        try:
            move = int(input("Choisissez une case : "))
        except ValueError:
            move = -1
        awale.play(player, move)
        player = 1 - player
        awale.game_over = awale.score[0] >= 24 or awale.score[1] >= 24 or (not awale.can_feed(player)[0] and
                                                                           not awale.can_feed(player)[1])
        print(awale.game_over)
    if awale.score[0] < 24 and awale.score[1] < 24:
        for i in range(12):
            awale.score[i // 6] += awale.board[i]
            awale.board[i] = 0
    print("Score du joueur 0 :", awale.score[0], "\nScore du joueur 1 :", awale.score[1])
    if awale.score[0] > awale.score[1]:
        print("Le joueur 0 a gagné !\n")
    elif awale.score[0] < awale.score[1]:
        print("Le joueur 1 a gagné !\n")
    else:
        print("Il y a égalité !\n")


game()


def create_tree(depth, br):
    """
    Crée un arbre de profondeur depth et avec br branches à chaque noeud.
    :return: arbre
    """
    return np.array([[[] for j in range(br ** i)] for i in range(depth + 1)])


def eval1(awale, player):
    """
    Affecte une valeur numérique à l'état actuel de la partie.
    :param awale: partie considérée
    :param player: numéro du joueur
    :return: évaluation de l'état actuel de la partie
    """
    return awale.score[player] - awale.score[1 - player]


def minmax(awale, eval, depth, player):
    if awale.game_over or depth == 0:
        return eval(awale, player)
    else:
        
