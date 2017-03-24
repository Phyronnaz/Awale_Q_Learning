import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsSimpleTextItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem


class HexView(QGraphicsView):
    def __init__(self, callback, *__args):
        QGraphicsView.__init__(self, *__args)
        self.callback = callback
        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        self.polygons = np.zeros(shape=12, dtype=object)
        self.old_polygons = np.zeros(shape=12, dtype=object)
        self.texts = np.zeros(shape=12, dtype=object)
        self.old_texts = np.zeros(shape=12, dtype=object)

        scale = 75

        for i in range(12):
            item = QGraphicsPolygonItemClick(i % 6, i // 6, scale, self.click, color="white")
            self.scene.addItem(item)
            self.polygons[i] = item

            t = QGraphicsSimpleTextItem("")
            t.setScale(3)
            t.setPos((i % 6 - 0.25) * scale, (i // 6 - 0.25) * scale)
            self.scene.addItem(t)
            self.texts[i] = t

            item = QGraphicsPolygonItemClick(i % 6, i // 6 - 4, scale, self.click, color="white")
            self.scene.addItem(item)
            self.old_polygons[i] = item

            t = QGraphicsSimpleTextItem("")
            t.setScale(3)
            t.setPos((i % 6 - 0.25) * scale, (i // 6 - 0.25 - 4) * scale)
            self.scene.addItem(t)
            self.old_texts[i] = t

    def click(self, i):
        self.callback(i)

    def set_board(self, board):
        board = board.copy()
        board[6:12] = board[6:12][::-1]
        for i in range(12):
            self.old_texts[i].setText(self.texts[i].text())
            self.texts[i].setText(str(board[i]))

    def set_board_colors(self, board, player):
        board = board.copy()
        if player == 1:
            board = board[::-1]
        maxi = np.max(np.abs(board))
        if maxi == 0:
            maxi = 1
        for i in range(6 * player, 6 * (player + 1)):
            r, g, b = 0, 0, 0
            v = board[i]
            a = int(abs(v) / maxi * 255)
            if v > 0:
                g = 255
            else:
                r = 255
            self.old_polygons[i].setColorRGB(*self.polygons[i].colors)
            self.polygons[i].setColorRGB(r, g, b, a)

    def set_color(self, i, color):
        self.polygons[i].set_color(color)


class QGraphicsPolygonItemClick(QGraphicsPolygonItem):
    def __init__(self, x, y, size, callback, color):
        self.colors = (0, 0, 0, 0)
        self.position = x if y == 0 else 11 - x
        self.callback = callback
        l = []
        for a in [(0.5, 0.5), (0.5, -0.5), (-0.5, -0.5), (-0.5, 0.5)]:
            i, j = a
            l.append(((x + i) * size, (y + j) * size))

        points = [QPointF(a, b) for (a, b) in l]
        polygon = QPolygonF(points)
        super().__init__(polygon)
        self.setPen(QPen(QColor("black"), size / 10))
        self.setBrush(QColor(color))

    def mousePressEvent(self, _):
        self.callback(self.position)

    def setColor(self, color):
        self.setBrush(QColor(color))

    def setColorRGB(self, r, g, b, a):
        self.colors = (r, g, b, a)
        self.setBrush(QColor(r, g, b, a))
