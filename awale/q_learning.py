import random
import warnings
from collections import deque

import numpy as np
import pandas as pd
import keras.models
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import RMSprop
from awale.main import *
from awale.negamax import get_move_negamax


def init_model():
    """
    Init model with size size
    :param size: size
    :return: model
    """
    model = Sequential()
    model.add(Dense(512, init='lecun_uniform', input_shape=(32 * 12,)))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(512, init='lecun_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(6, init='lecun_uniform'))
    model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    return model


def get_features(board, player):
    """
    Return the features corresponding to player
    :param board: board
    :param player: player
    :return: features
    """
    board = numpy.copy(board)
    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    state = -numpy.ones(32 * 12)
    for i in range(12):
        for j in range(board[i]):
            state[i * 32 + j] = 1
    return state


def get_action(model, split_board):
    """
    Get the move of a Q player
    :param model: model
    :param split_board: precomputed split board
    :return: q_values, action
    """
    # Predict
    [q_values] = model.predict(np.array([split_board]))

    # Get best action
    action = np.argmax(q_values)

    return action


def get_move_from_action(player, action):
    return action + player * 6


def get_move_q_learning(board, player, model):
    split_board = get_features(board, player)
    action = get_action(model, split_board)
    move = get_move_from_action(player, action)
    return move


def get_random_action(board: np.ndarray, state: np.random.RandomState, player: int):
    board = board.flatten()
    actions = [k[0] for k in numpy.argwhere(board != 0) if player * 6 <= k[0] < (player + 1) * 6]
    state.shuffle(actions)
    i = 0
    while not can_play(board, player, actions[i]):
        i += 1
    return actions[i] % 6


def learn(count, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size,
          q_players=(1,), allow_regret=(0, 1), initial_models_path=("", ""), thread=None):
    """
    Train the model
    :return: model, dataframe
    """

    ##################
    ### Load model ###
    ##################
    models = [None, None]

    for player in range(2):
        if player in q_players:
            if initial_models_path[player] == "":
                models[player] = init_model()
            else:
                models[player] = keras.models.load_model(initial_models_path[player])

    #####################
    ### Create arrays ###
    #####################
    n = (exploration_epochs + train_epochs) * 400
    epoch_array = np.zeros(n)
    winner_array = np.zeros(n)
    epsilon_array = np.zeros(n)
    random_move_array = np.zeros(n, dtype='bool')
    loss_array_player0 = np.zeros(n)
    loss_array_player1 = np.zeros(n)
    score_array_player0 = np.zeros(n)
    score_array_player1 = np.zeros(n)
    move_count_array = np.zeros(n)

    #######################
    ### Create memories ###
    #######################
    memories = [deque(), deque()]

    ###########################
    ### Initialize counters ###
    ###########################
    array_counter = 0
    last_array_counter = 0

    ######################
    ### Set parameters ###
    ######################
    epsilon = initial_epsilon
    epoch = 0
    frozen_players = []

    #######################
    ### Start main loop ###
    #######################
    while True:
        epoch += 1

        ##################
        ### Thread Log ###
        ##################
        if epoch % 10 == 0:
            thread.set_epoch(epoch)
            if epoch % 100 == 0:
                print("Epsilon: {}".format(epsilon))
                l = last_array_counter
                a = array_counter
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    loss_log_player0 = loss_array_player0[l:a][np.logical_not(np.isnan(loss_array_player0[l:a]))].mean()
                    loss_log_player1 = loss_array_player1[l:a][np.logical_not(np.isnan(loss_array_player1[l:a]))].mean()

                w = winner_array[l:a]
                c = (w != -1).sum()
                player0 = (w == 0).sum() / c * 100
                player1 = (w == 1).sum() / c * 100
                error = (w == 2).sum() / c * 100

                score0 = score_array_player0[l:a][winner_array[l:a] != -1].mean()
                score1 = score_array_player1[l:a][winner_array[l:a] != -1].mean()

                thread.log(epoch, loss_log_player0, loss_log_player1, player0, player1, error, score0, score1)
                last_array_counter = array_counter
                # if player0 > 75 and 0 in allow_freeze:
                #     frozen_players = [0]
                # elif player1 > 75 and 1 in allow_freeze:
                #     frozen_players = [1]
                # else:
                #     frozen_players = []

        #######################
        ### Break main loop ###
        #######################
        if epoch >= exploration_epochs + train_epochs or thread.stop:
            break

        ###################
        ### Set epsilon ###
        ###################
        if epsilon > final_epsilon:
            epsilon -= (initial_epsilon - final_epsilon) / exploration_epochs
        else:
            epsilon = final_epsilon

        ###############################################
        ### Create board and winner_check variables ###
        ###############################################
        board = init_board(count)
        score = [0, 0]
        winner = -2
        move_count = 0
        current_player = 0
        ai_random_state = np.random.RandomState()
        q_random_state = np.random.RandomState()

        #################################
        ### Initialize temp variables ###
        #################################
        actions = [None, None]
        states = [None, None]

        #################
        ### Game loop ###
        #################
        while True:
            random_move = np.nan
            losses = [np.nan, np.nan]
            delta_score = [0, 0]

            other_player = 1 - current_player
            current_player_is_q = current_player in q_players
            other_player_is_q = other_player in q_players
            current_player_is_learning = not current_player in frozen_players
            other_player_is_learning = not other_player in frozen_players

            ################################################
            ### If game already ended, just update model ###
            ################################################
            if winner == -2:
                ##################################
                ### Get move and save q values ###
                ##################################
                if current_player_is_q:
                    # Compute split board
                    split_board = get_features(board, current_player)

                    # Random move?
                    random_move = random.random() < epsilon

                    # Get action
                    if random_move:
                        if current_player in allow_regret:
                            action = np.random.randint(6)
                        else:
                            action = get_random_action(board, q_random_state, current_player)  # Limit regret
                    else:
                        action = get_action(models[current_player], split_board)

                    # Save action and split board
                    actions[current_player] = action
                    states[current_player] = split_board

                    # Get move
                    move = get_move_from_action(current_player, action)
                else:
                    random_move = random.random() < epsilon or True

                    # Get action
                    if random_move:
                        action = get_random_action(board, ai_random_state, current_player)
                        move = get_move_from_action(current_player, action)
                    else:
                        move = get_move_negamax(board, score, count, current_player, 1)

                ###################################
                ### Play move and update winner ###
                ###################################
                if can_play(board, current_player, move):
                    board, new_score = play(board, score, current_player, move)
                    winner = get_winner(board, score, winner, current_player)
                    delta_score = [new_score[i] - score[i] for i in range(2)]
                    score = new_score
                else:
                    winner = 2

            rewards = {"won": 0, "lost": 0, "error": -10,
                       "nothing": delta_score[current_player] - delta_score[other_player]}

            ######################
            ### Update players ###
            ######################
            if (other_player_is_q and other_player_is_learning and winner != 2 and move_count != 0) or \
                    (current_player_is_q and current_player_is_learning and winner == 2):
                if current_player_is_q and current_player_is_learning and winner == 2:
                    #
                    # Error: Update current player and quit
                    #
                    memory = memories[current_player]
                    action = actions[current_player]
                    old_state = states[current_player]
                    reward = rewards["error"]
                    terminal = True
                    new_state = None
                else:
                    #
                    # Update other player
                    #
                    memory = memories[other_player]
                    action = actions[other_player]
                    old_state = states[other_player]
                    # Get update
                    if winner == current_player:
                        reward = rewards["lost"]
                        terminal = True
                        new_state = None
                    elif winner == other_player:
                        reward = rewards["won"]
                        terminal = True
                        new_state = None
                    else:  # winner == -2
                        reward = rewards["nothing"]
                        terminal = False
                        new_state = get_features(board, other_player)
                #
                # Save to memory
                #
                # if len(memory) >= memory_size:
                #     memory.popleft()

                memory.append((old_state, action, new_state, reward, terminal))

            ########################
            ### Learn from memory ##
            ########################
            for player in range(2):
                model = models[player]
                memory = memories[player]
                if len(memory) >= memory_size:
                    X = np.zeros((batch_size, 32 * 12))
                    Y = np.zeros((batch_size, 6))

                    minibatch = random.sample(memory, batch_size)

                    for i in range(batch_size):
                        old_state, action, new_state, reward, terminal = minibatch[i]

                        [old_q_values] = model.predict(np.array([old_state]))

                        if terminal:
                            update = reward
                        else:
                            [new_q_values] = model.predict(np.array([new_state]))
                            update = reward + gamma * max(new_q_values)

                        old_q_values[action] = update

                        X[i] = old_state
                        Y[i] = old_q_values

                    losses[player] = model.train_on_batch(X, Y)
                    memory.clear()

            ###########
            ### Log ###
            ###########
            epoch_array[array_counter] = epoch
            winner_array[array_counter] = {(-2): -1, 0: 0, 1: 1, 2: 2}[winner]
            epsilon_array[array_counter] = epsilon
            random_move_array[array_counter] = random_move
            loss_array_player0[array_counter] = losses[0]
            loss_array_player1[array_counter] = losses[1]
            score_array_player0[array_counter] = score[0]
            score_array_player1[array_counter] = score[1]
            move_count_array[array_counter] = move_count

            ########################
            ### Update counters ###
            ########################
            array_counter += 1
            move_count += 1

            ######################
            ### Quit if needed ###
            ######################
            if winner == other_player or winner == -1 or winner == 2:
                if winner == -1:
                    print("draw")
                break

            #####################
            ### Invert player ###
            #####################
            current_player = other_player

    ########################
    ### Create dataframe ###
    ########################
    df = pd.DataFrame(dict(epoch=epoch_array[:array_counter],
                           winner=winner_array[:array_counter],
                           epsilon=epsilon_array[:array_counter],
                           random_move=random_move_array[:array_counter],
                           loss_player0=loss_array_player0[:array_counter],
                           loss_player1=loss_array_player1[:array_counter],
                           move_count=move_count_array[:array_counter]
                           ))
    ###########
    ### End ###
    ###########
    return models, df
