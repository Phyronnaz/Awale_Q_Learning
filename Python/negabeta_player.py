from negabeta import Negabeta


class NegabetaPlayer:
    def __init__(self, depth):
        self.depth = depth
        self.alpha = -float("inf")
        self.beta = float("inf")

    def get_move(self, awale, player):
        move = Negabeta.negabeta(awale, self.depth, player, self.alpha, self.beta)[1]

        return move
