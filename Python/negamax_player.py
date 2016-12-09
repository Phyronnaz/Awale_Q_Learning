from negamax import Negamax


class NegamaxPlayer:
    def __init__(self, depth):
        self.depth = depth

    def get_move(self, awale, player):
        move = Negamax.negamax(awale, self.depth, player)[1]

        return move
