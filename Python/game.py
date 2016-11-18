import numpy
from awale import Awale


class Game:
    """
    Permet de lancer une partie d'awalé.
    :return: aucun retour
    """

    def __init__(self, board=None, score=None):
        self.awale = Awale(board, score)
        self.player = 0
        self.game_over = False

    @staticmethod
    def display_rules():
        print("Le joueur 0 est au sud : il doit jouer les cases de 0 à 5.\n"
              "Le joueur 1 est au nord : il doit jouer les cases de 6 à 11.\n"
              "À tour de rôle, les joueurs doivent\n"
              "choisir une case de leur territoire puis distribuer dans le sens antihoraire les graines en les\n"
              "déposant une à une. Si la dernière graine est déposée dans le territoire adverse et que le trou\n"
              "contient alors 2 ou 3 graines, elles sont ramassées. On regarde de même les trous précédents,\n"
              "et on s'arrête dès qu'un trou contient 0, 1 ou plus de 4 graines. Le gagnant est celui qui a le plus\n"
              "de graines à la fin de la partie.")

    def update_game_over(self):
        self.game_over = self.awale.score[0] >= 24 or self.awale.score[1] >= 24 or (
            not self.awale.can_feed(self.player)[0] and not self.awale.can_feed(self.player)[1])

    def update_player(self):
        self.player = 1 - self.player

    def get_board(self):
        north = self.awale.board[6:12][::-1]
        south = self.awale.board[0:6]
        return numpy.array([north, south])

    def display_game(self):
        print(self.get_board())
        print("Score du joueur 0 :", self.awale.score[0], "\nScore du joueur 1 :", self.awale.score[1])
        print("\nC'est au joueur", self.player, "de jouer.")

    def get_move(self):
        # TODO: mettre ça dans can_play de l'awalé
        minmove = self.player * 6
        maxmove = (1 + self.player) * 6
        try:
            move = int(input("Choisissez une case : "))
        except ValueError:
            move = -1
        if self.awale.can_feed(self.player)[0] and not (self.awale.can_feed(self.player)[1]):
            while not (minmove <= move < maxmove) or self.awale.board[move] == 0:
                try:
                    move = int(input("Le coup est invalide, choisissez une autre case : "))
                except ValueError:
                    move = -1
        else:
            while not self.awale.can_play(self.player, move):
                try:
                    move = int(input("Le coup est invalide, choisissez une autre case : "))
                except ValueError:
                    move = -1
        return move

    def play(self):
        # TODO: mettre ça dans une méthode play de l'awalé
        move = self.get_move()
        will_starve = self.awale.can_feed(self.player)[0] and not (self.awale.can_feed(self.player)[1])
        if will_starve:
            self.awale.board = self.awale.deal(move)[0]
        else:
            self.awale.board, self.awale.score = self.awale.pick(self.player, move)
        self.update_player()
        self.update_game_over()

    def display_result(self):
        # TODO: check_game_over dans awalé
        if self.awale.score[0] < 24 and self.awale.score[1] < 24:
            for i in range(12):
                self.awale.score[i // 6] += self.awale.board[i]
                self.awale.board[i] = 0
        print("Score du joueur 0 :", self.awale.score[0], "\nScore du joueur 1 :", self.awale.score[1])
        if self.awale.score[0] > self.awale.score[1]:
            print("Le joueur 0 a gagné !\n")
        elif self.awale.score[0] < self.awale.score[1]:
            print("Le joueur 1 a gagné !\n")
        else:
            print("Il y a égalité !\n")
