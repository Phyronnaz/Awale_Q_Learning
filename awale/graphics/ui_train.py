from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from awale.graphics.plots import TrainPlot
from awale import hex_io
from awale.graphics.mainwindow import Ui_TIPE
from awale.threads.learn_thread import LearnThread


class TrainUI:
    def __init__(self, ui: Ui_TIPE):
        self.ui = ui
        self.create_plot()
        self.widgetPlot = self.ui.widgetTrainPlot  # type: TrainPlot

        # Connect update save folder
        self.ui.spinBoxSizeTrain.valueChanged.connect(self.update_save_name)
        self.ui.doubleSpinBoxGamma.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxBatchSize.valueChanged.connect(self.update_save_name)
        self.ui.doubleSpinBoxInitialEpsilon.valueChanged.connect(self.update_save_name)
        self.ui.doubleSpinBoxFinalEpsilon.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxExplorationEpochs.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxTrainEpochs.valueChanged.connect(self.update_save_name)
        self.ui.spinBoxMemory.valueChanged.connect(self.update_save_name)
        self.ui.checkBoxPlayer0.clicked.connect(self.update_save_name)
        self.ui.checkBoxPlayer1.clicked.connect(self.update_save_name)
        self.ui.checkBoxLearner0.clicked.connect(self.update_save_name)
        self.ui.checkBoxLearner1.clicked.connect(self.update_save_name)
        self.ui.checkBoxLoadPlayer0.clicked.connect(self.update_save_name)
        self.ui.checkBoxLoadPlayer1.clicked.connect(self.update_save_name)

        self.ui.checkBoxLoadPlayer0.clicked.connect(lambda: self.check_box_load(0))
        self.ui.checkBoxLoadPlayer1.clicked.connect(lambda: self.check_box_load(1))

        self.ui.checkBoxPlayer0.clicked.connect(lambda: self.check_box(0))
        self.ui.checkBoxPlayer1.clicked.connect(lambda: self.check_box(1))

        self.last_index = 0
        self.models = ["", ""]
        self.thread = None  # type: LearnThread

        self.ui.pushButtonChoosePlayer0.pressed.connect(lambda: self.choose_player(0))
        self.ui.pushButtonChoosePlayer1.pressed.connect(lambda: self.choose_player(1))
        self.ui.pushButtonTrain.pressed.connect(self.train_button)

        self.update_save_name()
        self.set_progress(-1)

        # Timer
        timer = QTimer(self.ui.centralWidget)
        timer.timeout.connect(self.update_train)
        timer.start(500)

    def create_plot(self):
        """
        Create the plot widget
        """
        self.ui.verticalLayoutTrainTab.removeWidget(self.ui.widgetTrainPlot)

        self.ui.widgetTrainPlot.deleteLater()

        self.ui.widgetTrainPlot = TrainPlot(self.ui.resultsTab, width=5, height=5, dpi=100)
        self.ui.widgetTrainPlot.setObjectName("widgetPlot")
        self.ui.verticalLayoutTrainTab.addWidget(self.ui.widgetTrainPlot)

    def update_plots(self):
        """
        Update the plots
        """
        if self.thread.index != self.last_index:
            self.last_index = self.thread.index

            # Clear
            self.widgetPlot.clear()

            # Plot
            self.widgetPlot.loss.plot(self.thread.epoch_log[:self.thread.index],
                                      self.thread.loss_log_player0[:self.thread.index], 'v-')
            self.widgetPlot.loss.plot(self.thread.epoch_log[:self.thread.index],
                                      self.thread.loss_log_player1[:self.thread.index], 'o-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.player0_log[:self.thread.index], 'v-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.player1_log[:self.thread.index], 'o-')
            self.widgetPlot.winner.plot(self.thread.epoch_log[:self.thread.index],
                                        self.thread.error_log[:self.thread.index], 'P-')
            self.widgetPlot.winner.set_ybound(0, 100)

            self.widgetPlot.score.plot(self.thread.epoch_log[:self.thread.index],
                                      self.thread.score0[:self.thread.index], 'v-')
            self.widgetPlot.score.plot(self.thread.epoch_log[:self.thread.index],
                                      self.thread.score1[:self.thread.index], 'o-')

            # Draw
            self.widgetPlot.draw()

    def set_progress(self, value, text=None):
        """
        Set Train progress bar value and text
        :param value: float between 0 and 1, negative to hide the bar
        :param text: text to display on the bar
        """
        if value < 0:
            self.ui.progressBarTrain.hide()
        else:
            self.ui.progressBarTrain.show()
            self.ui.progressBarTrain.setValue(100 * value)
            if text is not None:
                self.ui.progressBarTrain.setFormat(text)

    def choose_player(self, player):
        """
        Open file dialog to load model to continue training
        """
        f, g = QFileDialog.getOpenFileName(self.ui.centralWidget, "Open file", "", "Model (*.model)")

        if f != "":
            self.models[player] = f
            try:
                self.get_parameters(self.models[player])
            except ValueError:
                self.models[player] = ""
                msg_box = QMessageBox()
                msg_box.setText("Bad naming")
                msg_box.setWindowTitle("Error")
                msg_box.exec_()
            if player == 0:
                self.ui.lineEditLoadPlayer0.setText(self.models[player])
            else:
                self.ui.lineEditLoadPlayer1.setText(self.models[player])
        self.check_box_load(0)
        self.check_box_load(1)

    def train_button(self):
        """
        Handle train button click
        """
        if self.thread is None or not self.thread.learning:
            self.train()
        else:
            self.thread.stop = True

    def update_save_name(self):
        """
        Update save file name
        """
        self.ui.lineEditSaveName.setText(hex_io.save_dir + hex_io.get_save_name(*self.get_parameters()))

    def check_box(self, player):
        unchecked_0 = not self.ui.checkBoxPlayer0.isChecked()
        unchecked_1 = not self.ui.checkBoxPlayer1.isChecked()
        both_unchecked = unchecked_0 and unchecked_1
        if both_unchecked:
            if player == 0:
                self.ui.checkBoxPlayer0.setChecked(True)
            else:
                self.ui.checkBoxPlayer1.setChecked(True)
        self.update_save_name()

    def check_box_load(self, player):
        unchecked_0 = not self.ui.checkBoxLoadPlayer0.isChecked()
        unchecked_1 = not self.ui.checkBoxLoadPlayer1.isChecked()
        both_unchecked = unchecked_0 and unchecked_1

        self.ui.spinBoxSizeTrain.setEnabled(both_unchecked)
        self.ui.doubleSpinBoxGamma.setEnabled(both_unchecked)
        self.ui.spinBoxBatchSize.setEnabled(both_unchecked)
        self.ui.spinBoxMemory.setEnabled(both_unchecked)
        self.ui.checkBoxPlayer0.setEnabled(unchecked_0)
        self.ui.checkBoxPlayer1.setEnabled(unchecked_1)

        if (not unchecked_0 and player == 0) or (not unchecked_1 and player == 1):
            model = self.models[player]

            size, gamma, batch_size, _, _, _, _, memory_size, _, _ = self.get_parameters(model)
            self.ui.spinBoxSizeTrain.setValue(size)
            self.ui.doubleSpinBoxGamma.setValue(gamma)
            self.ui.spinBoxBatchSize.setValue(batch_size)
            self.ui.spinBoxMemory.setValue(memory_size)
            self.ui.checkBoxPlayer0.setChecked(not unchecked_0)
            self.ui.checkBoxPlayer1.setChecked(not unchecked_1)

    def get_parameters(self, model=""):
        """
        Get the parameters for train
        :return: size, gamma, batch_size, initial_epsilon, final_epsilon, exploration_epochs, train_epochs, memory_size, q_players, q_learners
        """
        b0, b1 = self.ui.checkBoxPlayer0.isChecked(), self.ui.checkBoxPlayer1.isChecked()
        c0, c1 = self.ui.checkBoxLearner0.isChecked(), self.ui.checkBoxLearner1.isChecked()
        if model == "":
            return self.ui.spinBoxSizeTrain.value(), \
                   self.ui.doubleSpinBoxGamma.value(), \
                   self.ui.spinBoxBatchSize.value(), \
                   self.ui.doubleSpinBoxInitialEpsilon.value(), \
                   self.ui.doubleSpinBoxFinalEpsilon.value(), \
                   self.ui.spinBoxExplorationEpochs.value(), \
                   self.ui.spinBoxTrainEpochs.value(), \
                   self.ui.spinBoxMemory.value(), \
                   [] + ([0] if b0 else []) + ([1] if b1 else []), \
                   [] + ([0] if c0 else []) + ([1] if c1 else [])

        else:
            d = hex_io.get_parameters_dict(model)
            size = d["size"]
            gamma = d["gamma"]
            batch_size = d["batch_size"]
            memory_size = d["memory_size"]

            return size, \
                   gamma, \
                   batch_size, \
                   self.ui.doubleSpinBoxInitialEpsilon.value(), \
                   self.ui.doubleSpinBoxFinalEpsilon.value(), \
                   self.ui.spinBoxExplorationEpochs.value(), \
                   self.ui.spinBoxTrainEpochs.value(), \
                   memory_size, \
                   [] + ([0] if b0 else []) + ([1] if b1 else []), \
                   [] + ([0] if c0 else []) + ([1] if c1 else [])

    def set_busy(self, busy):
        """
        Enable / Disable UI
        :param busy: budy
        """
        b = not busy
        self.ui.playTab.setEnabled(b)
        self.ui.resultsTab.setEnabled(b)
        self.ui.actionOpen.setEnabled(b)
        self.ui.horizontalLayoutInput.setEnabled(b)
        self.ui.horizontalLayoutLoad.setEnabled(b)
        self.ui.menuBar.setEnabled(b)

        if busy:
            self.ui.pushButtonTrain.setText("Stop")
        else:
            self.ui.pushButtonTrain.setText("Train")

    def update_train(self):
        """
        Update function called every 500ms
        """
        if self.thread is None:
            return
        self.update_plots()
        text = "Elapsed: {} | Remaining: {}".format(self.thread.elapsed_time, self.thread.remaining_time)
        self.set_progress(self.thread.get_progress(), text)
        if not self.thread.learning:
            self.end_thread()

    def train(self):
        """
        Start training
        """
        self.thread = LearnThread(self.get_parameters(), self.models)
        self.thread.start()
        self.set_busy(True)

    def end_thread(self):
        """
        Save model and quit thread
        """
        self.set_busy(False)
        self.set_progress(1, "Done")
        self.thread.join()
        self.thread = None
