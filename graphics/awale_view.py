import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsSimpleTextItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem


class AwaleView(QGraphicsView):
    def __init__(self, callback, *__args):
        QGraphicsView.__init__(self, *__args)
        self.callback = callback
        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        self.polygons = np.zeros(shape=12, dtype=object)
        self.texts = np.zeros(shape=12, dtype=object)

        self.scale = scale = 75

        for i in range(12):
            item = QGraphicsPolygonItemClick(i if i < 6 else (11 - i), i // 6, scale, self.click, i, color="white")
            self.scene.addItem(item)
            self.polygons[i] = item

            t = QGraphicsSimpleTextItem("4")
            s = 2
            t.setScale(s)
            t.setPos(scale * (i if i < 6 else (11 - i)) - t.boundingRect().width() * s / 2,
                     scale * (i // 6) - t.boundingRect().height() * s / 2)
            self.scene.addItem(t)
            self.texts[i] = t

    def click(self, i):
        self.callback(i)

    def set_board(self, board):
        for i in range(12):
            t = self.texts[i]
            t.setText(str(board[i]))
            t.setPos(self.scale * (i if i < 6 else (11 - i)) - t.boundingRect().width(),
                     self.scale * (i // 6) - t.boundingRect().height())

    def set_board_colors(self, board):
        maxi = np.max(np.abs(board))
        if maxi == 0:
            maxi = 1

        for i in range(12):
            t = self.texts[i]
            t.setText(str(round(board[i], 3)))
            t.setPos(self.scale * (i if i < 6 else (11 - i)) - t.boundingRect().width(),
                     self.scale * (i // 6) - t.boundingRect().height())

            r, g, b = 0, 0, 0
            v = board[i]
            a = int(abs(v) / maxi * 255)
            if v > 0:
                g = 255
            else:
                r = 255
            self.polygons[i].setColorRGB(r, g, b, a)

    def set_color(self, i, color):
        self.polygons[i].set_color(color)


class QGraphicsPolygonItemClick(QGraphicsPolygonItem):
    def __init__(self, x, y, scale, callback, position, color):
        self.colors = (0, 0, 0, 0)
        self.position = position
        self.callback = callback
        l = []
        for a in [(0.5, 0.5), (0.5, -0.5), (-0.5, -0.5), (-0.5, 0.5)]:
            i, j = a
            l.append(((x + i) * scale, (y + j) * scale))

        points = [QPointF(a, b) for (a, b) in l]
        polygon = QPolygonF(points)
        super().__init__(polygon)
        self.setPen(QPen(QColor("black"), scale / 10))
        self.setBrush(QColor(color))

    def mousePressEvent(self, _):
        self.callback(self.position)

    def setColor(self, color):
        self.setBrush(QColor(color))

    def setColorRGB(self, r, g, b, a):
        self.colors = (r, g, b, a)
        self.setBrush(QColor(r, g, b, a))
