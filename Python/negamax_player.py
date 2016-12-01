from negamax import Negamax


class NegamaxPlayer:
    def __init__(self, depth):
        self.depth = depth

    def get_move(self, awale, player):
        return Negamax.negamax(awale, self.depth, player, False)
