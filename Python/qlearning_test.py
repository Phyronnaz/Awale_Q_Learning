# Basé sur le tutoriel http://outlace.com/Reinforcement-Learning-Part-3/
# TODO : À finir, ne pas exécuter tel quel.
import numpy
import random
from awale import Awale
from random_player import RandomPlayer
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

model = Sequential()
model.add(Dense(164, init='lecun_uniform', input_shape=(48,)))
model.add(Activation('relu'))
# model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

model.add(Dense(150, init='lecun_uniform'))
model.add(Activation('relu'))
# model.add(Dropout(0.2))

model.add(Dense(6, init='lecun_uniform'))
model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

rms = RMSprop()
model.compile(loss='mse', optimizer=rms)

epochs = 3000
gamma = 0.7
epsilon = 1


# batchSize = 40
# buffer = 80
# replay = []
# stores tuples of (S, A, R, S')
# h = 0

def get_reward(awele, action, etat):
    if not awale.can_play(0, action):
        r = -8000
    else:
        if awele.winner == -2:
            r = 0
        elif awele.winner == -1:
            r = -10
        elif awele.winner == 0:
            r = 100
        elif awele.winner == 1:
            r = -100
        r += awele.score[0] - etat[1][0]
        r -= awele.score[1] - etat[1][1]

    return r


for e in range(epochs):
    print("epoch = {}".format(e))

    awale = Awale()
    moves_count = 0
    max_count = 400
    player = 0

    while awale.winner == -2 and moves_count < max_count:
        moves_count += 1

        if player == 0:
            # État S
            # Estimation du coup à jouer par le modèle
            state = awale.board, awale.score
            qval = model.predict(state[0].reshape(1, 12), batch_size=1)
            if random.random() < epsilon:  # choix d'un coup aléatoire
                move = random.randint(0, 5)
            else:  # choix du meileur coup d'après la prédiction du modèle
                move = numpy.argmax(qval)
            old_state = awale.board, awale.score
            awale.play(player, move)
            awale.check_winner(player)
            new_state = awale.board, awale.score
            # État S', obtention de la récompense
            reward = get_reward(awale, move, old_state)
            # Experience replay storage
            # if len(replay) < buffer:  # if buffer not filled, add to it
            #     replay.append((old_state, move, reward, new_state))
            # else:  # if buffer full, overwrite old values
            #     if h < (buffer - 1):
            #         h += 1
            #     else:
            #         h = 0
            #     replay[h] = (old_state, move, reward, new_state)
            #     # randomly sample our experience replay memory
            #     minibatch = random.sample(replay, batchSize)
            #     X_train = []
            #     y_train = []
            #     for memory in minibatch:
            #         # Get max_Q(S',a)
            #         old_state, move, reward, new_state = memory
            #         old_qval = model.predict(old_state[0].reshape(1, 12), batch_size=1)
            #         newQ = model.predict(new_state[0].reshape(1, 12), batch_size=1)
            #         maxQ = numpy.max(newQ)
            #         y = numpy.zeros((1, 6))
            #         y[:] = old_qval[:]
            #         if awale.winner != -2:  # non-terminal state
            #             update = (reward + (gamma * maxQ))
            #         else:  # terminal state
            #             update = reward
            #         y[0][move] = update
            #         X_train.append(old_state[0].reshape(12, ))
            #         y_train.append(y.reshape(6, ))
            #
            #     X_train = numpy.array(X_train)
            #     y_train = numpy.array(y_train)
            #     print("Game #: %s" % (i,))
            #     model.fit(X_train, y_train, batch_size=batchSize, nb_epoch=1, verbose=1)
            #     state = new_state
            if epsilon > 0.1:  # decrement epsilon over time
                epsilon -= (1 / epochs)
        else:
            move = RandomPlayer.get_move(awale, player)
            if awale.can_play(player, move):
                awale.play(player, move)
                awale.check_winner(player)
            else:
                raise Exception("Erreur! La case {} ne peut pas être jouée.".format(move))
        player = 1 - player
