import time

import keras.models

from game import Game
from q_player import QPlayer
from random_player import RandomPlayer

# game = Game(QPlayer(keras.models.load_model("/home/admin/qlearner.model")), RandomPlayer(), debug=True)
# t = time.clock()
# game.new_game()
# t = time.clock() - t
# print("Durée de la partie en minutes :", (t / 60))
# game.display_result()

model = keras.models.load_model("/home/admin/qlearner.model")

# for k in range(10000):
#     if k % 100 == 0: print(k)
#     mechant(model)


game = Game(QPlayer(model), RandomPlayer(), debug=True)
t = time.clock()
game.new_game()
t = time.clock() - t
print("Durée de la partie en minutes :", (t / 60))
game.display_result()