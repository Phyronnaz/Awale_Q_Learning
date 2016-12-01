class NewbiePlayer:
    @staticmethod
    def best_move(awale, player):
        minmove = player * 6
        maxmove = (1 + player) * 6
        possible_moves = []

        for i in range(minmove, maxmove):
            if awale.can_play(player, i):
                possible_moves.append(i)

        best_move = possible_moves[0]
        best_score = awale.pick(player, best_move)[1][player]

        for i in possible_moves[1:]:
            new_score = awale.pick(player, i)[1][player]
            if new_score > best_score:
                best_move = i

        return best_move

    @staticmethod
    def get_move(awale, player):
        move = -1

        while not awale.can_play(player, move):
            move = NewbiePlayer.best_move(awale, player)

        return move
