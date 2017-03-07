import keras.models
import numpy

from awale import Awale
from main import can_play

def get_state(board, player):
    board = numpy.copy(board)
    if player == 1:
        board = numpy.array([board[(i + 6) % 12] for i in range(12)])

    board[board == 0] = -1

    return board


def get_move(state, model):
    [q_values] = model.predict(numpy.array([state]))
    return numpy.argmax(q_values)

class QPlayer:
    def __init__(self, model):
        self.model = model  # keras.models.load_model(path)

    def get_move(self, awale: Awale, player):
        board = awale.board
        state = get_state(board, player)
        move = get_move(state, self.model) + 6 * player

        if can_play(board, [0, 0], player, move):
            return move
        else:
            raise Exception("Erreur: La case {} a disparue".format(move))
