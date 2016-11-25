import numpy
from game import Game
from random_player import RandomPlayer
from human_player import HumanPlayer
import matplotlib.pyplot as plt

game = Game(HumanPlayer(), HumanPlayer(), debug=True)
game.new_game()
