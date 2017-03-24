import numpy as np
from PyQt5 import QtGui
from awale import hex_io
from awale.game import Game
from awale.graphics import debug
from awale.graphics.hex_view import HexView
from awale.graphics.mainwindow import Ui_TIPE


class PlayUI:
    def __init__(self, ui: Ui_TIPE):
        # Hack
        ui.spinBoxSizePlay.setValue(3)

        # Variables
        self.size = -1
        self.game = None
        self.models = []

        self.ui = ui

        # Initial states
        self.ui.pushButtonViewDefault.setChecked(True)
        self.ui.pushButtonViewPlayer1.setChecked(False)
        self.ui.pushButtonViewPlayer2.setChecked(False)

        self.ui.pushButtonPlay.setEnabled(False)

        # Connect actions
        self.ui.spinBoxSizePlay.valueChanged.connect(self.update_size)

        self.ui.comboBoxPlayer1.activated.connect(self.update_combo_box)
        self.ui.comboBoxPlayer2.activated.connect(self.update_combo_box)

        self.ui.pushButtonViewDefault.clicked.connect(self.update_graphics_views)
        self.ui.pushButtonViewPlayer1.clicked.connect(self.update_graphics_views)
        self.ui.pushButtonViewPlayer2.clicked.connect(self.update_graphics_views)

        self.ui.pushButtonPlay.clicked.connect(self.play_button)
        self.ui.pushButtonPlay.setShortcut("Return")
        self.ui.pushButtonNewGame.clicked.connect(self.new_game)

        # Launch update functions
        self.set_progress(-1)
        self.update_models_list()
        self.update_combo_box()
        self.update_size()

    def reload_graphics_views(self):
        """
        Recreate HexViews
        """
        hints = QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing | \
                QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.TextAntialiasing

        self.ui.horizontalLayoutPlayTab.removeWidget(self.ui.graphicsViewDefault)
        self.ui.horizontalLayoutPlayTab.removeWidget(self.ui.graphicsViewPlayer1)
        self.ui.horizontalLayoutPlayTab.removeWidget(self.ui.graphicsViewPlayer2)

        self.ui.graphicsViewDefault.deleteLater()
        self.ui.graphicsViewPlayer1.deleteLater()
        self.ui.graphicsViewPlayer2.deleteLater()

        self.ui.graphicsViewDefault = HexView(self.click, self.ui.playTab)
        self.ui.graphicsViewPlayer1 = HexView(self.click, self.ui.playTab)
        self.ui.graphicsViewPlayer2 = HexView(self.click, self.ui.playTab)

        self.ui.graphicsViewDefault.setEnabled(True)
        self.ui.graphicsViewPlayer1.setEnabled(True)
        self.ui.graphicsViewPlayer2.setEnabled(True)

        self.ui.graphicsViewDefault.setRenderHints(hints)
        self.ui.graphicsViewPlayer1.setRenderHints(hints)
        self.ui.graphicsViewPlayer2.setRenderHints(hints)

        self.ui.graphicsViewDefault.setObjectName("graphicsViewDefault")
        self.ui.graphicsViewPlayer1.setObjectName("graphicsViewPlayer1")
        self.ui.graphicsViewPlayer2.setObjectName("graphicsViewPlayer2")

        self.ui.horizontalLayoutPlayTab.addWidget(self.ui.graphicsViewDefault)
        self.ui.horizontalLayoutPlayTab.addWidget(self.ui.graphicsViewPlayer1)
        self.ui.horizontalLayoutPlayTab.addWidget(self.ui.graphicsViewPlayer2)

    def update_size(self):
        """
        Apply size change
        """
        self.size = self.ui.spinBoxSizePlay.value()
        self.reload_graphics_views()
        self.update_graphics_views()
        self.game = None
        self.update_game()
        self.update_models_list()

    def update_combo_box(self):
        """
        Apply player change
        """
        if self.ui.comboBoxPlayer1.currentIndex() == 1:
            self.ui.labelMinimaxDepthPlayer1.show()
            self.ui.spinBoxMinimaxDepthPlayer1.show()
        else:
            self.ui.labelMinimaxDepthPlayer1.hide()
            self.ui.spinBoxMinimaxDepthPlayer1.hide()

        if self.ui.comboBoxPlayer2.currentIndex() == 1:
            self.ui.labelMinimaxDepthPlayer2.show()
            self.ui.spinBoxMinimaxDepthPlayer2.show()
        else:
            self.ui.labelMinimaxDepthPlayer2.hide()
            self.ui.spinBoxMinimaxDepthPlayer2.hide()

    def update_models_list(self):
        """
        Update list of the models and players choice
        """

        self.ui.listWidgetModels.clear()
        self.ui.listWidgetModels.addItems([hex_io.get_pretty_name(*hex_io.get_parameters(m)) for m in self.models])

        pretty_names = [hex_io.get_pretty_name(*hex_io.get_parameters(n)) for n in self.models if
                        hex_io.get_parameters_dict(n)["size"] == self.size]
        players = ["Human", "Minimax", "Random"] + pretty_names

        self.ui.comboBoxPlayer1.clear()
        self.ui.comboBoxPlayer2.clear()

        self.ui.comboBoxPlayer1.addItems(players)
        self.ui.comboBoxPlayer2.addItems(players)

    def update_graphics_views(self):
        """
        Enable/Disable HexViews
        """
        if self.ui.pushButtonViewDefault.isChecked():
            self.ui.graphicsViewDefault.show()
        else:
            self.ui.graphicsViewDefault.hide()

        if self.ui.pushButtonViewPlayer1.isChecked():
            self.ui.graphicsViewPlayer1.show()
        else:
            self.ui.graphicsViewPlayer1.hide()

        if self.ui.pushButtonViewPlayer2.isChecked():
            self.ui.graphicsViewPlayer2.show()
        else:
            self.ui.graphicsViewPlayer2.hide()

    def update_game(self):
        """
        Update UI after a move
        """
        self.update_boards()
        b = self.game is not None and self.game.winner == -2 and self.game.players[self.game.player][0] != "Human"
        self.ui.pushButtonPlay.setEnabled(b)

    def update_boards(self):
        """
        Update HexViews
        """
        if self.game is not None:
            self.ui.graphicsViewDefault.set_board(self.game.board)
            self.ui.graphicsViewPlayer1.set_board_colors(self.game.aux_boards[0], 0)
            self.ui.graphicsViewPlayer2.set_board_colors(-self.game.aux_boards[1], 1)

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
            self.game.click(i)
            self.update_game()

    def set_progress(self, value, text=None):
        """
        Set MiniMax progress bar value and text
        :param value: float between 0 and 1, negative to hide the bar
        :param text: text to display on the bar
        """
        if value < 0:
            self.ui.progressBarMinimax.hide()
        else:
            self.ui.progressBarMinimax.show()
            self.ui.progressBarMinimax.setValue(100 * value)
            if text is not None:
                self.ui.progressBarMinimax.setFormat(text)

    def new_game(self):
        """
        Create a new game
        """
        combos = self.ui.comboBoxPlayer1.currentIndex(), self.ui.comboBoxPlayer2.currentIndex()
        depths = self.ui.spinBoxMinimaxDepthPlayer1.value(), self.ui.spinBoxMinimaxDepthPlayer2.value()
        players = [None, None]
        for i in range(2):
            if combos[i] == 0:
                players[i] = "Human", ""
            elif combos[i] == 1:
                players[i] = "Minimax", depths[i]
            elif combos[i] == 2:
                players[i] = "Random", ""
            else:
                players[i] = "Q learning", self.models[combos[i] - 3]
        print("Size: {}".format(self.size))
        self.game = Game(self.size, players)
        self.update_game()
        debug.debug_play("New Game")

    def add_model(self, path):
        """
        Add a model
        :param path: path of the model to add
        """
        if path not in self.models:
            self.models.append(path)
            self.update_models_list()
