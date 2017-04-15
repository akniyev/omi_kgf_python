from PyQt5.QtCore import QSize, QRect
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.Qt import *

from PlotLab.Classes.View.DiagramItem import DiagramItem


class BoxDiagramItem(DiagramItem):
    def __init__(self):
        super().__init__()
        self.size = QSize(50, 50)

    def get_my_rect(self):
        parent_cx = 0
        parent_cy = 0
        if self.parent is not None:
            parent_cx = self.parent.center.x()
            parent_cy = self.parent.center.y()
        cx = self.center.x() + parent_cx
        cy = self.center.y() + parent_cy
        sw = self.size.width()
        sh = self.size.height()
        rect = QRect(cx - sw / 2, cy - sh / 2, sw, sh)
        return rect

    def point_hit_check(self, x, y):
        return self.get_my_rect().contains(x, y)

    def draw(self, qp: QPainter):
        rect = self.get_my_rect()
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(QColor("red" if self.selected else "gray"))
        pen = QPen(QColor("blue" if self.hover else "black"))
        pen.setWidth(3 if self.hover else 1)
        qp.setPen(pen)
        qp.fillRect(rect, brush)
        qp.drawRect(rect)

