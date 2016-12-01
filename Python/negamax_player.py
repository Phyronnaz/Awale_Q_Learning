from negamax import Negamax

class NegamaxPlayer:
    @staticmethod
    def get_move(awale,depth,player):
        return Negamax.negamax(awale,depth,player,False)
