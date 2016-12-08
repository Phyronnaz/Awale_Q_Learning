from alphabeta import Alphabeta

class AlphabetaPlayer:
    def __init__ (self,depth):
        self.depth = depth
        self.alpha = -float("inf")
        self.beta = float("inf")

    def get_move (self,awale,player):
        return Alphabeta.alphabeta(awale,self.depth,player,self.alpha,self.beta)[1]
