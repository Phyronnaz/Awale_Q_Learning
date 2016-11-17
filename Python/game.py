import numpy
from awale import Awale


def game():
    """
    Lance une partie d'awalé.
    :return: aucun retour
    """
    awale = Awale()
    player = 0
    print("Le joueur 0 est au sud : il doit jouer les cases de 0 à 5.\n"
          "Le joueur 1 est au nord : il doit jouer les cases de 6 à 11.\n")
    awale.game_over = awale.score[0] >= 24 or awale.score[1] >= 24 or (not awale.can_feed(player)[0] and
                                                                       not awale.can_feed(player)[1])
    while not awale.game_over:
        north = awale.board[6:12][::-1]
        south = awale.board[0:6]
        board = numpy.array([north, south])
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
