import numpy as np
from PyQt5 import QtGui
import tensorflow as tf
import keras
from main import *
from game import Game
from graphics.awale_view import AwaleView
from graphics.mainwindow import Ui_TIPE
from q_learning import get_features


class PlayUI:
    def __init__(self, ui: Ui_TIPE):
        # Variables
        self.game = None
        self.models = ["Human"]

        self.ui = ui

        # Initial states
        self.ui.pushButtonViewPlayer1.setChecked(False)
        self.ui.pushButtonViewPlayer2.setChecked(False)

        self.ui.pushButtonPlay.setEnabled(False)

        self.ui.pushButtonViewPlayer1.clicked.connect(self.update_graphics_views)
        self.ui.pushButtonViewPlayer2.clicked.connect(self.update_graphics_views)

        self.ui.pushButtonPlay.clicked.connect(self.play_button)
        self.ui.pushButtonPlay.setShortcut("Return")
        self.ui.pushButtonNewGame.clicked.connect(self.new_game)

        # Launch update functions
        self.reload_graphics_views()
        self.update_models_list()
        self.update_graphics_views()

    def reload_graphics_views(self):
        """
        Recreate HexViews
        """
        hints = QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing | \
                QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.TextAntialiasing

        self.ui.horizontalLayout.removeWidget(self.ui.graphicsViewDefault)
        self.ui.horizontalLayout.removeWidget(self.ui.graphicsViewPlayer1)
        self.ui.horizontalLayout.removeWidget(self.ui.graphicsViewPlayer2)

        self.ui.graphicsViewDefault.deleteLater()
        self.ui.graphicsViewPlayer1.deleteLater()
        self.ui.graphicsViewPlayer2.deleteLater()

        self.ui.graphicsViewDefault = AwaleView(self.click, self.ui.centralWidget)
        self.ui.graphicsViewPlayer1 = AwaleView(self.click, self.ui.centralWidget)
        self.ui.graphicsViewPlayer2 = AwaleView(self.click, self.ui.centralWidget)

        self.ui.graphicsViewDefault.setEnabled(True)
        self.ui.graphicsViewPlayer1.setEnabled(True)
        self.ui.graphicsViewPlayer2.setEnabled(True)

        self.ui.graphicsViewDefault.setRenderHints(hints)
        self.ui.graphicsViewPlayer1.setRenderHints(hints)
        self.ui.graphicsViewPlayer2.setRenderHints(hints)

        self.ui.graphicsViewDefault.setObjectName("graphicsViewDefault")
        self.ui.graphicsViewPlayer1.setObjectName("graphicsViewPlayer1")
        self.ui.graphicsViewPlayer2.setObjectName("graphicsViewPlayer2")

        self.ui.horizontalLayout.addWidget(self.ui.graphicsViewDefault)
        self.ui.horizontalLayout.addWidget(self.ui.graphicsViewPlayer1)
        self.ui.horizontalLayout.addWidget(self.ui.graphicsViewPlayer2)

    def update_models_list(self):
        """
        Update list of the models and players choice
        """

        self.ui.comboBoxPlayer1.clear()
        self.ui.comboBoxPlayer2.clear()

        self.ui.comboBoxPlayer1.addItems(self.models)
        self.ui.comboBoxPlayer2.addItems(self.models)

    def update_graphics_views(self):
        """
        Enable/Disable HexViews
        """
        if self.ui.pushButtonViewPlayer1.isChecked():
            self.ui.graphicsViewPlayer1.show()
        else:
            self.ui.graphicsViewPlayer1.hide()

        if self.ui.pushButtonViewPlayer2.isChecked():
            self.ui.graphicsViewPlayer2.show()
        else:
            self.ui.graphicsViewPlayer2.hide()

        self.update_boards()

    def update_game(self):
        """
        Update UI after a move
        """
        self.update_boards()
        b = self.game is not None and self.game.winner == -2 and self.game.players[self.game.player] != "Human"
        self.ui.pushButtonPlay.setEnabled(b)

    def update_boards(self):
        """
        Update HexViews
        """
        if self.game is not None:
            self.ui.graphicsViewDefault.set_board(self.game.board)
            if self.ui.pushButtonViewPlayer1.isChecked():
                self.ui.graphicsViewPlayer1.set_board_colors(self.get_aux_board(0))
            if self.ui.pushButtonViewPlayer2.isChecked():
                self.ui.graphicsViewPlayer2.set_board_colors(self.get_aux_board(1))

    def play_button(self):
        """
        Handle play button click
        """
        if self.game is not None:
            self.game.play()
            self.update_game()

    def click(self, i):
        """
        Handle a click on the tile with coordinate x y
        :param x: x
        :param y: y
        """
        if self.game is not None:
            # print("Click {}".format(i))
            self.game.click(i)
            self.update_game()

    def new_game(self):
        """
        Create a new game
        """
        combos = self.ui.comboBoxPlayer1.currentIndex(), self.ui.comboBoxPlayer2.currentIndex()
        players = [self.models[i] for i in combos]
        self.game = Game(players)
        self.update_game()
        print("New game")

    def add_model(self, path):
        """
        Add a model
        :param path: path of the model to add
        """
        if path not in self.models:
            self.models.append(path)
            self.update_models_list()

    def get_aux_board(self, player):
        name = self.game.players[player]
        if name == "Human":
            return np.zeros(12)
        else:
            config = tf.ConfigProto()
            sess = tf.Session(config=config)
            keras.backend.set_session(sess)
            with sess.graph.as_default():
                model = keras.models.load_model(name)

                board_0 = invert(self.game.board, 0)
                board_1 = invert(self.game.board, 1)

                [q_values_0] = model.predict(np.array([get_features(board_0)]))
                [q_values_1] = model.predict(np.array([get_features(board_1)]))

            l = np.zeros(12)
            l[:6] = q_values_0
            l[6:] = q_values_1

            return l
