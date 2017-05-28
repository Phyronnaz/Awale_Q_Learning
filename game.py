import keras.models
from main import *
from negamax.negamax import get_move_negamax
from q_learning import get_action, get_features


class Game:
    def __init__(self, players):
        """
        Create Game
        """
        # Assign variables
        self.players = players

        # Init game
        self.board = init_board()
        self.player = 0
        self.winner = -2
        self.scores = [0, 0]
        self.models = [None, None]

        for i in range(2):
            if self.players[i][0] not in ["Human", "Minimax"]:
                self.models[i] = keras.models.load_model(self.players[i][0])

    def play_move(self, move):
        if self.winner == -2:
            i_board = invert(self.board, self.player)
            if can_play(i_board, move):
                i_board, score = play(i_board, move)

                self.scores[self.player] += score
                self.board = invert(i_board, self.player)

                self.winner = get_winner(self.board, self.scores, self.winner, self.player)
                self.player = 1 - self.player
            else:
                print("Failed to play! Move: {}".format(move))

            print("Scores: {}".format(self.scores))

            if self.winner != -2:
                print("Winner: {}".format(self.winner))

    def play(self):
        name, depth = self.players[self.player]
        if name == "Human":
            return
        elif name == "Minimax":
            s = self.scores if self.player == 0 else self.scores[::-1]
            self.play_move(get_move_negamax(invert(self.board, self.player), s, 4, 0, depth))
        else:
            i_board = invert(self.board, self.player)
            move = get_action(self.models[self.player], get_features(i_board))

            self.play_move(move)

    def click(self, i):
        if self.players[self.player][0] == "Human":
            if self.player * 6 <= i < (self.player + 1) * 6:
                return self.play_move(i % 6)
