import matplotlib.lines as mlines
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ResultsPlot(FigureCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.loss = self.fig.add_subplot(221)
        self.winner = self.fig.add_subplot(222)
        self.epsilon = self.fig.add_subplot(223)
        self.legend = self.fig.legend([], [], 'lower right')
        self.fig.set_tight_layout(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.names = []
        self.plot_enabled = []
        self.colors = []
        self.name_plots()
        self.draw()

    def name_plots(self):
        # Epsilon
        self.epsilon.set_title("Epsilon")
        self.epsilon.set_xlabel("epoch")
        self.epsilon.set_ylabel("epsilon")

        # Loss
        self.loss.set_title("Loss")
        self.loss.set_xlabel("epoch")
        self.loss.set_ylabel("loss")

        # Winner
        self.winner.set_title("Winner")
        self.winner.set_xlabel("epoch")
        self.winner.set_ylabel("percentage")
        self.winner.set_ybound(0, 100)

        labels = ["Player 0", "Player 1", "error"]
        markers = ["v", "o", "P"]
        colors = ["black", "black", "black"]
        lines = []
        for i in range(len(colors)):
            lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
        self.winner.legend(handles=lines)

        # Legend
        lines = []
        for i in range(len(self.names)):
            if self.plot_enabled[i]:
                lines.append(mlines.Line2D([], [], color=self.colors[i], label=self.names[i], marker="o"))
        self.legend.remove()
        l = [self.names[i] for i in range(len(self.names)) if self.plot_enabled[i]]
        self.legend = self.fig.legend(lines, l, 'lower right')

    def clear(self):
        self.epsilon.cla()
        self.loss.cla()
        self.winner.cla()
        self.name_plots()


class TrainPlot(FigureCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.loss = self.fig.add_subplot(131)
        self.winner = self.fig.add_subplot(132)
        self.score = self.fig.add_subplot(133)
        self.fig.set_tight_layout(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.names = []
        self.enabled = []
        self.colors = []
        self.name_plots()

    def name_plots(self):
        # Loss
        self.loss.set_title("Loss")
        self.loss.set_xlabel("epoch")
        self.loss.set_ylabel("loss")

        # Winner
        self.winner.set_title("Winner")
        self.winner.set_xlabel("epoch")
        self.winner.set_ylabel("percentage")
        self.winner.set_ybound(0, 100)

        labels = ["Player 0", "Player 1", "error"]
        markers = ["v", "o", "P"]
        colors = ["black", "black", "black"]
        lines = []
        for i in range(len(colors)):
            lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
        self.winner.legend(handles=lines)

        # Score
        self.score.set_title("Scores")
        self.score.set_xlabel("epoch")
        self.score.set_ylabel("score")

        labels = ["Player 0", "Player 1"]
        markers = ["v", "o"]
        colors = ["black", "black"]
        lines = []
        for i in range(len(colors)):
            lines.append(mlines.Line2D([], [], color=colors[i], label=labels[i], marker=markers[i]))
        self.score.legend(handles=lines)

        self.draw()

    def clear(self):
        self.loss.cla()
        self.winner.cla()
        self.score.cla()
        self.name_plots()
