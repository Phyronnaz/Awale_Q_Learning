from getopt import getopt
import sys
import os

path = os.path.dirname(os.path.realpath(__file__))[:-8]
if path not in sys.path:
    sys.path.insert(0, path)

from PyQt5 import QtWidgets
from awale.graphics import UI
from awale import hex_io
from awale.threads.learn_thread import LearnThread


def iterator(s: str, f):
    l = s.split(":")
    if len(l) == 1:
        yield f(s)
    elif len(l) == 3:
        [start, end, step] = f(l[0]), f(l[1]), f(l[2])
        x = start
        while x < end:
            yield f(str(x))
            x += step
    else:
        raise ValueError


def get_value(l, s):
    for t in l:
        if t[0] == "--" + s:
            return t[1]
    print(s + " is missing")
    raise ValueError


if len(sys.argv) == 1:
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
else:
    size = 3
    gamma = 0.75
    batch_size = 64
    initial_epsilon = 0.75
    final_epsilon = 0.001
    exploration_epochs = 750000
    train_epochs = 250000
    memory_size = 64
    q_players = [0]
    parameters = (size, gamma, batch_size, initial_epsilon, final_epsilon,
                  exploration_epochs, train_epochs, memory_size, q_players, [])

    print(hex_io.get_pretty_name(*(parameters + ("all",))))
    thread = LearnThread(parameters, ["", ""])
    thread.run()


    # args = ["size=", "gamma=", "initial_epsilon=", "final_epsilon=", "exploration_epochs=", "train_epochs=",
    #         "memory_size=", "batch_size=", "name=", "first_q", "second_q"]
    # try:
    #     l = getopt(sys.argv[1:], "", args)[0]
    #
    #     try:
    #         name = get_value(l, "name")
    #         hex_io.save_dir += name + "/"
    #     except ValueError:
    #         pass
    #
    #     first_q = ("--first_q", '') in l
    #     second_q = ("--second_q", '') in l
    #
    #     q_players = [] + ([0] if first_q else []) + ([1] if second_q else [])
    #
    #     f = lambda n: lambda s: round(float(s), n)
    #
    #     size_iterator = iterator(get_value(l, "size"), int)
    #     for size in size_iterator:
    #         gamma_iterator = iterator(get_value(l, "gamma"), f(2))
    #         for gamma in gamma_iterator:
    #             initial_epsilon_iterator = iterator(get_value(l, "initial_epsilon"), f(5))
    #             for initial_epsilon in initial_epsilon_iterator:
    #                 final_epsilon_iterator = iterator(get_value(l, "final_epsilon"), f(5))
    #                 for final_epsilon in final_epsilon_iterator:
    #                     exploration_epoch_iterator = iterator(get_value(l, "exploration_epochs"), int)
    #                     for exploration_epochs in exploration_epoch_iterator:
    #                         train_epochs_iterator = iterator(get_value(l, "train_epochs"), int)
    #                         for train_epochs in train_epochs_iterator:
    #                             memory_size_iterator = iterator(get_value(l, "memory_size"), int)
    #                             for memory_size in memory_size_iterator:
    #                                 batch_size_iterator = iterator(get_value(l, "batch_size"), int)
    #                                 for batch_size in batch_size_iterator:
    #                                     parameters = (size, gamma, batch_size, initial_epsilon, final_epsilon,
    #                                                   exploration_epochs, train_epochs, memory_size, q_players, [])
    #
    #                                     print(hex_io.get_pretty_name(*(parameters + ("all",))))
    #                                     thread = LearnThread(parameters, ["", ""])
    #                                     thread.run()
    # except ValueError as e:
    #     print(e)
    #     print(args)
