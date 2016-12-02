import numpy
from awale import Awale


class Game:
    """
    Permet de lancer une partie d'awalé.
    """

    def __init__(self, player0, player1, board=None, score=None, debug=True, max_count=400):
        """
        :param board: plateau de jeu initial si différent du plateau de début de partie
        :param score: score de jeu initial si différent du score de début de partie
        """
        self.awale = Awale(board, score)
        self.players = [player0, player1]
        self.debug = debug
        self.moves_count = 0
        self.max_count = max_count

    @staticmethod
    def display_rules():
        """
        Affiche un bref rappel des règles de l'awalé.
        :return: aucun retour
        """
        print("Le joueur 0 est au sud : il doit jouer les cases de 0 à 5.\n"
              "Le joueur 1 est au nord : il doit jouer les cases de 6 à 11.\n"
              "À tour de rôle, les joueurs doivent choisir une case de leur territoire puis distribuer dans le sens"
              " antihoraire les graines en les déposant une à une.\n"
              "Si la dernière graine est déposée dans le territoire adverse et que le trou contient alors 2 ou 3"
              " graines, ces dernières sont ramassées par le joueur.\n"
              "On regarde de même les trous précédents, et on s'arrête dès qu'un trou contient 0, 1 ou plus de 4"
              " graines ou qu'on revient au territoire du joueur.\n"
              "Le gagnant est celui qui a le plus de graines à la fin de la partie.\n")

    def get_board(self):
        """
        :return: plateau de jeu sur deux rangées
        """
        north = self.awale.board[6:12][::-1]
        south = self.awale.board[0:6]

        return numpy.array([north, south])

    def display_board(self):
        """
        Affiche le plateau de jeu
        :return: aucun retour
        """
        print(self.get_board())

    def display_score(self):
        """
        Affiche le score de chaque joueur.
        :return: aucun retour
        """
        print("Score du joueur 0 :", self.awale.score[0], "\nScore du joueur 1 :", self.awale.score[1])

    def display_result(self):
        """
        Affiche le résultat de la partie.
        :return: aucun retour
        """
        if self.awale.score[0] < 24 and self.awale.score[1] < 24:
            self.awale.get_seeds()
        self.display_score()
        if self.awale.score[0] > self.awale.score[1]:
            print("Le joueur 0 a gagné !\n")
        elif self.awale.score[0] < self.awale.score[1]:
            print("Le joueur 1 a gagné !\n")
        else:
            print("Il y a égalité !\n")

    def new_game(self):
        """
        Lance une partie d'awalé. La partie s'arrête si le nombre de coups joués dépasse max_count.
        :return: aucun retour
        """
        if self.debug:
            self.display_rules()

        # self.awale = Awale(board=numpy.array([1, 0, 0, 0, 0, 1, 4, 0, 3, 0, 0, 1]), score=numpy.array([17, 21]))
        self.awale = Awale()
        self.moves_count = 0
        player = 0

        while self.awale.winner == -2 and self.moves_count < self.max_count:
            self.moves_count += 1

            if self.debug:
                self.display_board()
                self.display_score()
                minmove = player * 6
                maxmove = (1 + player) * 6
                print("C'est au joueur", player, "de jouer."
                                                 " Choisissez une case entre {} et {}.".format(minmove, maxmove - 1))

            move = self.players[player].get_move(self.awale, player)
            if self.awale.can_play(player, move):
                self.awale.play(player, move)
                self.awale.check_winner(player)
                if self.debug:
                    print("Le joueur {} a joué la case {}.".format(player, move))
            else:
                raise Exception("Erreur! La case {} ne peut pas être jouée.".format(move))
            player = 1 - player

        if self.debug:
            self.display_result()
