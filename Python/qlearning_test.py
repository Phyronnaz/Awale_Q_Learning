# Basé sur le tutoriel http://outlace.com/Reinforcement-Learning-Part-3/
import random

import matplotlib.pyplot as plt
import numpy
from keras.layers.core import Dense, Activation
from keras.models import Sequential
from keras.optimizers import RMSprop

from game import Game
from awale.awale import Awale
from main import init_board, play, can_play, get_winner
from q_player import QPlayer
from random_player import RandomPlayer


def init_model():
    model = Sequential()
    model.add(Dense(512, init='lecun_uniform', input_shape=(32 * 12,)))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))

    model.add(Dense(6, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


def get_state(board, player):
    board = numpy.copy(board)
    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    state = -numpy.ones(32 * 12)
    for i in range(12):
        for j in range(board[i]):
            state[i * 32 + j] = 1
    return state


def get_moves(board, score, player):
    board = numpy.copy(board)
    minmove = player * 6
    maxmove = (1 + player) * 6
    moves = -numpy.ones(6)
    for i in range(minmove, maxmove):
        if can_play(board, score, player, i):
            moves[i] = 1
    return moves


def get_input_array(board, score, player):
    state = get_state(board, player)
    moves = get_moves(board, score, player)
    return state


def get_move(input_array, model):
    [q_values] = model.predict(numpy.array([input_array]))
    return numpy.argmax(q_values)


def f():
    exploration_epochs = 1000000
    final_epochs = 0
    epochs = exploration_epochs + final_epochs
    gamma = 0.9
    initial_epsilon = 0.75
    final_epsilon = 0.01
    epsilon = initial_epsilon

    losses = []
    winners = []
    score0 = []
    score1 = []
    nbre_coups = []

    model = init_model()

    for epoch in range(epochs):
        if epoch % 100 == 0:
            print("epoch = {}".format(epoch))

        if epsilon > final_epsilon:
            epsilon -= (initial_epsilon - final_epsilon) / exploration_epochs
        else:
            epsilon = final_epsilon

        moves_count = 0
        max_count = 400
        board = init_board()
        board[:] = 3
        score = [0, 0]
        winner = -2
        player = 0

        old_input_array, old_move, reward = None, None, None

        while winner == -2 and moves_count < max_count:
            moves_count += 1

            if player == 0:
                input_array = get_input_array(board, score, player)

                # Trouver le coup
                if random.random() < epsilon:
                    move = numpy.random.randint(6)
                else:
                    move = get_move(input_array, model)

                # Sauvegarder
                old_input_array, old_move = input_array, move
            else:
                move = RandomPlayer.get_move(Awale(board, score), player)

            if can_play(board, score, player, move):
                board, new_score = play(board, score, player, move)

                delta_score = [new_score[i] - score[i] for i in range(2)]
                score = new_score

                winner = get_winner(board, score, winner, player)
            else:
                winner = -3

            winners.append(winner)

            if player == 0:
                reward = {-3: -10, -2: delta_score[0], -1: 10, 0: 100, 1: -5}[winner]

            if player == 1 or winner != -2:
                [old_q_values] = model.predict([numpy.array([old_input_array])])

                if winner == -2:
                    new_input_array = get_input_array(board, score, 0)
                    [new_q_values] = model.predict([numpy.array([new_input_array])])

                    old_q_values[old_move] = reward + gamma * max(new_q_values)
                else:
                    old_q_values[old_move] = reward

                X = numpy.array([old_input_array])
                Y = numpy.array([old_q_values])
                loss = model.train_on_batch(X, Y)
                losses.append(loss)

            player = 1 - player
        score0.append(score[0])
        score1.append(score[1])
        nbre_coups.append(moves_count)
        if moves_count >= max_count:
            print("La partie est trop longue.")

    model.save("/home/admin/qlearner.model")

    n = epochs // 25
    x = [i * n for i in range(25)]

    plt.subplot(221)
    plt.plot(x, [numpy.array(losses[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
    plt.xlabel("Époque")
    plt.ylabel("Loss")

    winner0 = numpy.zeros(100)
    winner1 = numpy.zeros(100)
    error = numpy.zeros(100)
    winners = numpy.array(winners)

    losses = numpy.array(losses)
    score0 = numpy.array(score0)
    score1 = numpy.array(score1)

    numpy.save("/home/admin/losses.npy", losses)
    numpy.save("/home/admin/score0.npy", score0)
    numpy.save("/home/admin/score1.npy", score1)

    print("G: {}, P: {}".format(sum(winners == 0), sum(winners == 1)))

    for i in range(100):
        w = winners[i * n:(i + 1) * n]
        p = sum(w != -2)
        winner0[i] = sum(w == 0) * 100 / p
        winner1[i] = sum(w == 1) * 100 / p
        error[i] = sum(w == -3) * 100 / p

    xx = [i * n for i in range(100)]

    plt.subplot(222)
    plt.plot(xx, winner0, "-o", label="Pourentage de parties gagnées par QPlayer", color="blue")
    plt.plot(xx, winner1, "-o", label="Pourentage de parties gagnées par NewbiePlayer", color="green")
    plt.plot(xx, error, "-o", label="Pourcentage de parties terminées pour coup invalide", color="red")
    plt.xlabel("Époque")
    plt.legend()

    plt.subplot(223)
    plt.plot(x, [numpy.array(score0[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
    plt.xlabel("Époque")
    plt.ylabel("Score moyen de QPlayer")

    plt.subplot(224)
    plt.plot(x, [numpy.array(score1[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
    plt.xlabel("Époque")
    plt.ylabel("Score moyen de RandomPlayer")
    plt.show()
    plt.plot(x, [numpy.array(nbre_coups[i * n:(i + 1) * n]).mean() for i in range(25)], "-o")
    plt.show()

    game = Game(QPlayer(model), RandomPlayer(), debug=True)
    game.new_game()
    game.display_result()


def mechant(model):
    board = numpy.random.randint(0, 12, size=12)
    board[6:12] = 0

    score = [0, 0]
    player = 0
    winner = -2
    gamma = 0.9

    input_array = get_input_array(board, score, player)

    # Trouver le coup
    move = get_move(input_array, model)

    # Sauvegarder
    old_input_array, old_move = input_array, move

    if can_play(board, score, player, move):
        board, new_score = play(board, score, player, move)

        delta_score = [new_score[i] - score[i] for i in range(2)]
        score = new_score

        winner = get_winner(board, score, winner, player)
    else:
        winner = -3

    reward = {-3: -10, -2: 0, -1: 10, 0: 100, 1: -5}[winner]



    if winner != -2:
        [old_q_values] = model.predict([numpy.array([old_input_array])])
        old_q_values[old_move] = reward
        X = numpy.array([old_input_array])
        Y = numpy.array([old_q_values])
        loss = model.train_on_batch(X, Y)


if __name__ == "__main__":
    f()
