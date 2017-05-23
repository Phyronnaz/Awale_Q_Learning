import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from graphics.mainwindow import Ui_TIPE
from graphics.ui_play import PlayUI


class UI:
    def __init__(self):
        # Window
        self.TIPE = QtWidgets.QMainWindow()
        self.ui = Ui_TIPE()
        self.ui.setupUi(self.TIPE)
        self.TIPE.setWindowTitle("TIPE Hex")
        self.TIPE.show()

        # Subclasses
        self.playUI = PlayUI(self.ui)

        # Connect actions
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionOpen.setShortcut("Ctrl+O")

    def open(self):
        name_filter = "Model (*.model)"

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter(name_filter)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            for f in fileNames:
                if os.path.exists(f):
                    self.playUI.add_model(f)
                elif f != "":
                    msg_box = QMessageBox()
                    msg_box.setText("File does not exist")
                    msg_box.setWindowTitle("Error")
                    msg_box.exec_()
