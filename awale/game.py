import keras.models
import numpy as np
import tensorflow as tf
from awale.main import *
from awale.q_learning import get_move_q_learning, get_features, get_random_action, get_move_from_action
from awale.negamax import get_move_negamax
from awale.graphics import debug


class Game:
    def __init__(self, count, players):
        """
        Create Game
        :param count: size of the board
        :param players: list of "Name", "Paramater" ("Human", "" or "Minimax", 12 or "Q leaning", model_path)
        """
        # Assign variables
        self.players = players
        self.ended = False
        self.size = count

        # Init game
        self.board = init_board(count)
        self.player = 0
        self.winner = -2
        self.score = [0, 0]

        self.aux_boards = [np.zeros(12), np.zeros(12)]

        self.depths = [0, 0]
        self.random_states = [np.random.RandomState(), np.random.RandomState()]

        for i in range(2):
            if players[i][0] == "Minimax":
                self.depths[i] = players[i][1]

    def play_move(self, move):
        if self.winner == -2:
            if can_play(self.board, self.player, move):
                self.board, self.score = play(self.board, self.score, self.player, move)
                self.winner = get_winner(self.board, self.score, self.winner, self.player)
                self.player = 1 - self.player
                debug.debug_play("Score: {} | {}".format(self.score[0], self.score[1]))
            else:
                debug.debug_play("Failed to play!")
        if self.winner != -2 and not self.ended:
            self.ended = True
            debug.debug_play("Winner: Player %s" % self.winner)

    def play(self):
        name, _ = self.players[self.player]
        if name == "Human":
            return
        elif name == "Minimax":
            move = get_move_negamax(self.board, self.score, self.size, self.player, self.depths[self.player])
            # self.aux_boards[self.player] = values
            self.play_move(move)
        elif name == "Random":
            action = get_random_action(self.board, self.random_states[self.player], self.player)
            move = get_move_from_action(self.player, action)
            self.play_move(move)
        elif name == "Q learning":
            config = tf.ConfigProto()
            sess = tf.Session(config=config)
            keras.backend.set_session(sess)
            with sess.graph.as_default():
                model = keras.models.load_model(self.players[self.player][1])

                move = get_move_q_learning(self.board, self.player, model)

                [q_values] = model.predict(np.array([get_features(self.board, self.player)]))

            if self.player == 1:
                q_values = [q_values[(k + 6) % 12] for k in range(12)]
            self.aux_boards[self.player] = q_values

            self.play_move(move)

    def click(self, i):
        if self.players[self.player][0] == "Human":
            return self.play_move(i)
