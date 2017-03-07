# Basé sur le tutoriel http://outlace.com/Reinforcement-Learning-Part-3/
# TODO : À finir, ne pas exécuter tel quel.
import numpy
import random

from keras.callbacks import History

from awale import Awale
from game import Game
from human_player import HumanPlayer
from main import init_board, play, can_play, get_winner
from newbie_player import NewbiePlayer
from q_player import QPlayer
from random_player import RandomPlayer
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt


def init_model():
    model = Sequential()
    model.add(Dense(64, init='lecun_uniform', input_shape=(12,)))
    model.add(Activation('relu'))

    model.add(Dense(64, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(6, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


def get_state(board, player):
    board = numpy.copy(board)

    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    board[board == 0] = -1

    return board


def get_move(state, model):
    [q_values] = model.predict(numpy.array([state]))
    return numpy.argmax(q_values)


epochs = 10000
gamma = 0.1
epsilon = 1

losses = []
winners = []

model = init_model()

for epoch in range(epochs):
    if epoch % 100 == 0:
        print("epoch = {}".format(epoch))

    if epsilon > 0.1:  # decrement epsilon over time
        epsilon -= 1 / epochs

    moves_count = 0
    max_count = 400
    board = init_board()
    score = [0, 0]
    winner = -2
    player = 0

    old_state, old_move, reward = None, None, None

    while winner == -2 and moves_count < max_count:
        moves_count += 1

        if player == 0:
            state = get_state(board, player)

            # Trouver le coup
            if random.random() < epsilon:
                move = numpy.random.randint(6)  # Limite regret
            else:
                move = get_move(state, model)

            # Sauvegarder
            old_state, old_move = state, move
        else:
            move = NewbiePlayer.get_move(Awale(board, score), player)

        if can_play(board, score, player, move):
            board, new_score = play(board, score, player, move)

            delta_score = [new_score[i] - score[i] for i in range(2)]
            score = new_score

            winner = get_winner(board, score, winner, player)
        else:
            winner = -3

        winners.append(winner)

        if player == 0:
            reward = {-3: -10, -2: delta_score[0] / 48 - delta_score[1] / 48, -1: 0, 0: 5, 1: -5}[winner]

        if player == 1 or winner != -2:
            [old_q_values] = model.predict([numpy.array([old_state])])

            if winner == -2:
                new_state = get_state(board, 0)
                [new_q_values] = model.predict([numpy.array([new_state])])

                old_q_values[old_move] = reward + gamma * max(new_q_values)
            else:
                old_q_values[old_move] = reward

            X = numpy.array([old_state])
            Y = numpy.array([old_q_values])
            loss = model.train_on_batch(X, Y)
            losses.append(loss)

        player = 1 - player
    if moves_count >= max_count:
        print("coucou")

# model.save("coucou.model")

x = [k * len(winners) // 25 for k in range(25)]

plt.subplot(211)
plt.plot(x,
         [numpy.array(losses[i * len(winners) // 25:(i + 1) * len(winners) // 25]).mean() for i in range(25)], "-o")

plt.subplot(212)

winner0 = numpy.zeros(25)
winner1 = numpy.zeros(25)
error = numpy.zeros(25)

winners = numpy.array(winners)

for i in range(25):
    l = winners[i * len(winners) // 25:(i + 1) * len(winners) // 25]
    n = sum(l != -2)
    winner0[i] = sum(l == 0) / n
    winner1[i] = sum(l == 1) / n
    error[i] = sum(l == -3) / n

plt.plot(x, winner0, "-o", color="blue")
plt.plot(x, winner1, "-o", color="green")
plt.plot(x, error, "-o", color="red")

plt.show()

game = Game(QPlayer(model), NewbiePlayer(), debug=True)
game.new_game()
game.display_result()
