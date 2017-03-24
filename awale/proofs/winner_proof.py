import numpy

from awale.main import play_move, init_board, has_win
from awale.winner_check import check_for_winner, init_winner_matrix_and_counter
from awale.main import get_random_move

size = 11

win_count_has_win = 0
win_count_winner_check = 0
n = 100

rs = numpy.random.RandomState()
for i in range(n):
    if i % 10 == 0:
        print(i)
    board = init_board(size)
    winner_matrix, winner_counter = init_winner_matrix_and_counter(size)
    w = False
    p = 0
    while not w:
        move = get_random_move(board, rs)
        play_move(board, move, p)
        hw = has_win(board, p)
        winner, winner_counter = check_for_winner(move, p, winner_matrix, winner_counter)
        w = hw or winner != -1
        if hw:
            win_count_has_win += 1
        if winner != - 1:
            win_count_winner_check += 1
        p = (p + 1) % 2

print("{} games played".format(n))
print("{} % of the games are ok".format((n - abs(win_count_has_win - win_count_winner_check)) * 100 / n))
