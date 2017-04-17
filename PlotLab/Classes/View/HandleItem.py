from enum import Enum
from typing import List, Set

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QTextOption
from PyQt5.Qt import  *

from PlotLab.Classes.View.DiagramItem import DiagramItem, DragType


class HandleType(Enum):
    Input = -1
    Output = 1


class HandleItem(DiagramItem):
    def __init__(self):
        super().__init__()
        self.radius = 5
        self.name = ""
        self.type: HandleType = HandleType.Input
        self.movable = DragType.Line
        from PlotLab.Classes.View.LineItem import LineItem
        self.output_lines: Set[LineItem] = set()
        self.input_line: LineItem = None
        self.out_value = None

    def get_lines(self):
        return list(self.output_lines) + ([] if self.input_line is None else [self.input_line])

    def point_hit_check(self, x, y):
        c = self.global_center()
        return (c.x() - x) ** 2 + (c.y() - y) ** 2 <= self.radius ** 2

    def draw(self, qp: QPainter):
        c = self.global_center()
        r = self.radius
        pen = QPen(QColor("black"))
        pen.setWidth(1 if not self.hover else 3)
        qp.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        if self.type == HandleType.Output:
            brush.setColor(QColor("red" if self.out_value is None else "green"))
        elif self.type == HandleType.Input:
            brush.setColor(QColor("orange" if self.input_line is None or self.input_line.source.out_value is None else "blue"))
        qp.setBrush(brush)
        qp.drawEllipse(QRect(c.x() - r, c.y() - r, 2 * r, 2 * r))
        text_rect = QRectF(c.x() + r, c.y() - 2 * r, 2 * r, 4 * r) if self.type == HandleType.Input else QRectF(c.x() - 3*r, c.y() - 2 * r, 2 * r, 4 * r)
        qp.drawText(text_rect, self.radius, self.name)
