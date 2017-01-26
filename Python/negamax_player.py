from negamax import Negamax


class NegamaxPlayer:
    def __init__(self, depth, evaluation):
        self.depth = depth
        self.evaluation = evaluation

    def get_move(self, awale, player):
        move = Negamax.negamax(awale, self.depth, player, self.evaluation)[1]

        return move
