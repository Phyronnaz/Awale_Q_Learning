from negamax import negamax


class NegamaxPlayer:
    def __init__(self, depth, evaluation):
        self.depth = depth
        self.evaluation = evaluation

    def get_move(self, awale, player):
        move = negamax(awale, self.depth, player, self.evaluation)[1]

        return move
