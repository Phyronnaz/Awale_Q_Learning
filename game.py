import keras.models
import numpy as np
import tensorflow as tf
from main import *
from q_learning import get_action, get_features


class Game:
    def __init__(self, players):
        """
        Create Game
        """
        # Assign variables
        self.players = players

        # Init game
        self.board = init_board()
        self.player = 0
        self.winner = -2
        self.scores = [0, 0]

    def play_move(self, move):
        if self.winner == -2:
            i_board = invert(self.board, self.player)
            if can_play(i_board, move):
                i_board, score = play(i_board, move)

                self.scores[self.player] += score
                self.board = invert(i_board, self.player)

                self.winner = get_winner(self.board, self.scores, self.winner)
                self.player = 1 - self.player
            else:
                print("Failed to play! Move: {}".format(move))

            print("Scores: {}".format(self.scores))

            if self.winner != -2:
                print("Winner: {}".format(self.winner))

    def play(self):
        name = self.players[self.player]
        if name == "Human":
            return
        else:
            config = tf.ConfigProto()
            sess = tf.Session(config=config)
            keras.backend.set_session(sess)
            with sess.graph.as_default():
                model = keras.models.load_model(name)

                i_board = invert(self.board, self.player)
                move = get_action(model, get_features(i_board))

            self.play_move(move)

    def click(self, i):
        if self.players[self.player] == "Human":
            if self.player * 6 <= i < (self.player + 1) * 6:
                return self.play_move(i % 6)
