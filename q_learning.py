import os
import random
from collections import deque

import keras.models
import numpy as np
import pandas as pd
from keras.layers.core import Dense, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import RMSprop

from main import *


def init_model():
    """
    Init model 
    :return: model
    """

    model = Sequential()

    model.add(Dense(512, input_dim=48 * 12, kernel_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(512, kernel_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(512, kernel_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(512, kernel_initializer="lecun_uniform"))
    model.add(Activation('relu'))

    model.add(Dense(6, kernel_initializer="lecun_uniform"))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


def get_features(board):
    """
    Return features of board
    :param board: board
    :return: features
    """

    t = -np.ones((12, 48))

    t[np.arange(12), board.T] = 1

    return t.flatten()


def get_action(model: keras.models.Model, features: np.ndarray) -> int:
    """
    Get the move of a Q player
    :param model: model
    :param features: precomputed split board
    :return: q_values, action
    """
    # Predict
    [q_values] = model.predict(np.array([features]))

    # Get best action
    action = np.argmax(q_values)

    return action


def get_random_action(board: np.ndarray) -> int:
    l = list(range(6))
    np.random.shuffle(l)

    i = 0

    while not can_play(board, l[i]):
        i += 1

    return l[i]


def best_action(board):
    i = 0
    while not can_play(board, i):
        i += 1

    best_score = pick(board, i)[1]
    best = i

    while i < 6:
        if can_play(board, i):
            score = pick(board, i)[1]
            if score > best_score:
                best_score = score
                best = i
        i += 1

    return best


def create_database(n):
    boards = deque()
    actions = deque()
    for i in range(n):
        if i % 100 == 0:
            print("Creating database: {}% ({})".format(round(100 * i / n, 2), i))

        board = init_board()
        scores = [0, 0]
        winner = -2

        while winner == -2:
            action = best_action(board)

            boards.append(board.copy())
            actions.append(action)

            if random.random() < 1 / 4:
                action = get_random_action(board)

            board, score = play(board, action)
            scores[0] += score

            winner = get_winner(board, scores, winner, 0)

            board = invert_players(board)

    return np.array([boards, actions])


def train(model, database):
    X, Y = database

    n = len(X)

    def f(a, b):
        l = np.zeros((len(b), 6))
        for i in range(len(l)):
            l[i][b[i]] = pick(a[i], b[i])[1]
        return np.array([get_features(board) for board in a]), l

    m = n // 10
    for i in range(m):
        if i % 100 == 0:
            print("Training: {}% ({})".format(round(100 * i / m, 2), i))
        l = random.sample(range(n), 64)
        model.train_on_batch(*f(X[l], Y[l]))


def learn(gamma, epochs, memory_size, batch_size, model_path="", thread=None):
    """
    Train the model
    :return: model, dataframe
    """

    ##########################
    ## Create/Load database ##
    ##########################
    path = os.path.expanduser("~") + "/Awale/database.npy"
    if os.path.exists(path):
        database = np.load(path)
    else:
        database = create_database(10000)
        np.save(path, database)

    ##################
    ### Load model ###
    ##################
    if model_path == "":
        model = init_model()
        # train(model, database)
    else:
        model = keras.models.load_model(model_path)

    #####################
    ### Create arrays ###
    #####################
    winner_array = np.zeros(epochs)
    loss_array = np.zeros(epochs)
    move_count_array = np.zeros(epochs)
    score_array = np.zeros(epochs)

    thread.winner_array = winner_array
    thread.loss_array = loss_array

    #######################
    ### Create memories ###
    #######################
    memory = deque()

    ###########################
    ### Initialize counters ###
    ###########################
    index = 0

    ######################
    ### Set parameters ###
    ######################
    epsilon = 0.1
    epoch = 1  # avoid problems with %

    #######################
    ### Main loop ###
    #######################
    while epoch < epochs and not thread.stop:
        ##################
        ### Thread Log ###
        ##################
        if epoch % 10 == 0:
            thread.set_epoch(epoch)

        ########################
        ### Learn from memory ##
        ########################
        loss = np.nan
        if len(memory) >= batch_size:  # enough experiences
            X = np.zeros((batch_size, 48 * 12))
            Y = np.zeros((batch_size, 6))

            batch = random.sample(memory, batch_size)

            old_states = np.array([b[0] for b in batch])
            new_states = np.array([b[2] for b in batch])

            old_q_values = model.predict(old_states)
            new_q_values = model.predict(new_states)

            for i in range(batch_size):
                _, action, _, reward, terminal = batch[i]

                if terminal:
                    update = reward
                else:
                    update = reward - gamma * max(new_q_values[i])

                old_q_values[i][action] = update

                X[i] = old_states[i]
                Y[i] = old_q_values[i]

            loss = model.train_on_batch(X, Y)

        ###############################################
        ### Create board and winner_check variables ###
        ###############################################
        board = init_board()
        score = 0
        winner = -2
        move_count = 0

        #################
        ### Game loop ###
        #################
        while winner == -2 and move_count < 1000:
            move_count += 1

            ##################################
            ### Get move and save q values ###
            ##################################
            # Compute features
            features = get_features(board)

            # Random move?
            random_move = random.random() < epsilon

            # Get action
            if random_move:
                action = get_random_action(board)  # Limit regret by not choosing completely random action
            else:
                action = get_action(model, features)

            #################
            ### Play move ###
            #################
            if can_play(board, action):
                board, s = play(board, action)
                score += s
            else:
                winner = 2

            winner = get_winner(board, [score / 2, score / 2], winner, 0)

            ##################
            ## Invert board ##
            ##################
            board = invert_players(board)

            ####################
            ## Save to memory ##
            ####################
            if len(memory) == memory_size:
                memory.popleft()
            old_state = features
            new_state = get_features(board)

            terminal = winner != -2

            if winner == 2:
                reward = -24
            else:
                reward = s

            memory.append((old_state, action, new_state, reward, terminal))

        if move_count >= 1000:
            print("Max move count!")

        ###########
        ### Log ###
        ###########
        winner_array[index] = winner
        loss_array[index] = loss
        move_count_array[index] = move_count
        score_array[index] = score

        ########################
        ### Update counters ###
        ########################
        index += 1

        #######################
        ### Increment epoch ###
        #######################
        epoch += 1

    ########################
    ### Create dataframe ###
    ########################
    df = pd.DataFrame(dict(winner=winner_array[:index],
                           loss=loss_array[:index],
                           move_count=move_count_array[:index],
                           score=score_array[:index],
                           ))
    ###########
    ### End ###
    ###########
    return model, df
