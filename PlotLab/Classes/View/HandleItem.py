from enum import Enum

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QPen, QColor

from PlotLab.Classes.View.DiagramItem import DiagramItem


class HandleType(Enum):
    Input = -1
    Output = 1


class HandleItem(DiagramItem):
    def __init__(self):
        super().__init__()
        self.radius = 5
        self.name = ""
        self.type = HandleType.Input

    def point_hit_check(self, x, y):
        c = self.global_center()
        return (c.x() - x) ** 2 + (c.y() - y) ** 2 <= self.radius ** 2

    def draw(self, qp: QPainter):
        c = self.global_center()
        r = self.radius
        pen = QPen(QColor("black"))
        pen.setWidth(1 if not self.hover else 3)
        qp.drawEllipse(QRect(c.x() - r, c.y() - r, 2 * r, 2 * r))
