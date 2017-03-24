import numpy

from awale.awale import Awale
from main import can_play


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



class QPlayer:
    def __init__(self, model):
        self.model = model  # keras.models.load_model(path)

    def get_move(self, awale: Awale, player):
        board = awale.board
        score = awale.score
        input_array = get_input_array(board, score, player)
        move = get_move(input_array, self.model) + 6 * player

        if can_play(board, score, player, move):
            return move
        else:
            raise Exception("Erreur! La case {} ne peut pas être jouée.".format(move))
