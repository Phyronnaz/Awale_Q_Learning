import sys
from PyQt5 import QtWidgets

from graphics.ui import UI

app = QtWidgets.QApplication(sys.argv)
ui = UI()
sys.exit(app.exec_())