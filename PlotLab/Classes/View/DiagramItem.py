from enum import Enum
from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter

from PlotLab.Classes.View.HandleItem import HandleItem


class DiagramItem:
    def __init__(self):
        self.parent: DiagramItem = None
        self.hover = False
        self.selected = False
        self.center = QPoint()
        self.movable = True

    def global_center(self):
        if self.parent is None:
            return self.center
        else:
            return self.center + self.parent.global_center()

    def get_children(self) -> List[HandleItem]:
        return []

    def point_hit_check(self, x, y) -> bool:
        return False

    def draw(self, qp: QPainter):
        pass




