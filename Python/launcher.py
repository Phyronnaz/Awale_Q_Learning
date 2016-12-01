from game import Game
from human_player import HumanPlayer
from newbie_player import NewbiePlayer

game = Game(NewbiePlayer(), HumanPlayer())
game.new_game()
