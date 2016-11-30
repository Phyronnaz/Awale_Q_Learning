import numpy
import matplotlib.pyplot as plt
from game import Game
from random_player import RandomPlayer

n = 5000
max_moves = numpy.zeros(n)
game = Game(RandomPlayer(), RandomPlayer(), debug=False)
over400 = numpy.zeros(10)
mean_moves = numpy.zeros(10)

for k in range(10):
    for i in range(n):
        if i % (n / 10) == 0:
            print(i)
        game.new_game()
        max_moves[i] = game.moves_count
    N = numpy.arange(1001)
    games_N = numpy.array([(max_moves == i).sum() for i in N])

    plt.clf()
    plt.stem(N, games_N)
    plt.xlabel("N = Nombre de coups joués pour finir la partie")
    plt.ylabel("Nombre de parties finies en N coups")
    plt.savefig("img{}".format(k))
    over400[k] = games_N[401:1001].sum()
    mean_moves[k] = max_moves.mean()

print((over400 / 50).mean())  # Résultats = en moyenne 0.77 % au-dessus de 400 coups.
print(mean_moves.mean())  # Résultats = en moyenne 104 coups pour finir la partie.
