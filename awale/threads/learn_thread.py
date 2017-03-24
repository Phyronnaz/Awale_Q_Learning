import threading
import datetime
import numpy as np
from awale import hex_io
from awale.q_learning import learn
import keras.backend
import tensorflow as tf


class LearnThread(threading.Thread):
    def __init__(self, parameters, models):
        threading.Thread.__init__(self)

        self.n = parameters[5] + parameters[6]

        self.parameters = parameters
        self.models = models

        self.epoch_log = np.zeros(self.n)
        self.loss_log_player0 = np.zeros(self.n)
        self.loss_log_player1 = np.zeros(self.n)
        self.player0_log = np.zeros(self.n)
        self.player1_log = np.zeros(self.n)
        self.error_log = np.zeros(self.n)
        self.score0 = np.zeros(self.n)
        self.score1 = np.zeros(self.n)
        self.index = 0

        self.start_time = datetime.datetime.now()
        self.elapsed_time = ""
        self.remaining_time = ""
        self.current_epoch = 0

        self.stop = False
        self.learning = False

    def run(self):
        self.stop = False
        self.learning = True
        print("Learning started")
        config = tf.ConfigProto()
        sess = tf.Session(config=config)
        keras.backend.set_session(sess)
        with sess.graph.as_default():
            hex_io.save_models_and_df(*learn(*self.parameters, self.models, thread=self), *self.parameters)
        print("Learning ended")
        self.learning = False

    def get_progress(self):
        """
        Return progress of the learning
        :return: float between 0 and 1
        """
        return self.current_epoch / self.n

    def log(self, epoch, loss_log_player0, loss_log_player1, player0, player1, error, score0, score1):
        """
        Add a row to the logs
        :param epoch: epoch
        :param loss: loss
        :param player0: percentage of game player 0 won
        :param player1: percentage of game player 1 won
        :param error: percentage of game ended with an error
        """
        self.epoch_log[self.index] = epoch
        self.loss_log_player0[self.index] = loss_log_player0
        self.loss_log_player1[self.index] = loss_log_player1
        self.player0_log[self.index] = player0
        self.player1_log[self.index] = player1
        self.error_log[self.index] = error
        self.score0[self.index] = score0
        self.score1[self.index] = score1
        self.index += 1

    def set_epoch(self, epoch):
        """
        Set epoch of the training
        :param epoch: epoch
        """
        self.current_epoch = epoch

        elapsed = int((datetime.datetime.now() - self.start_time).seconds)
        total = int(elapsed * self.n / (epoch + 1))

        self.elapsed_time = datetime.timedelta(seconds=elapsed)
        self.remaining_time = datetime.timedelta(seconds=max(total - elapsed, 0))

        print("Current epoch: {}; Remaining time: {}; Elapsed time: {}".format(self.current_epoch, self.remaining_time,
                                                                               self.elapsed_time))
