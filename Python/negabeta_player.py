from negabeta import Negabeta


class NegabetaPlayer:
    def __init__(self, depth,evaluation):
        self.depth = depth
        self.alpha = -float("inf")
        self.beta = float("inf")
        self.evaluation = evaluation

    def get_move(self, awale, player):
        move = Negabeta.negabeta(awale, self.depth, player, self.alpha, self.beta, self.evaluation)[1]

        return move
