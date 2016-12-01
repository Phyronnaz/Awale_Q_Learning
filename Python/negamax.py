import numpy
from awale import Awale

class Minmax:
    """
    créer l'arbre et renvoie le trou optimal à jouer
    """

    @staticmethod

    def negamax(awale,depth,player):
        if awale.game_over or depth==0:
            return(awale.evaluation1(player))
        else:
            best_score = float("inf")
            best_move = float("inf")
            possible_move =[]
            for i in range (6*player,6*(1+player)):
                if awale.can_play(player,i):
                    possible_move.append(i)
            for j in possible_move:
                new_board, new_score = awale.pick(player, j)
                score = -Minmax.negamax(Awale(new_board,new_score),depth-1,player)
                if score>=best_score:
                    best_score=score
                    best_move=j
        return(best_move)