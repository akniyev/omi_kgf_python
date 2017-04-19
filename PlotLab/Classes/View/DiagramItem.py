from enum import Enum
from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter


class DragType(Enum):
    Movable = 0
    Immovable = 1
    Line = 2


class DiagramItem:
    __id = 0

    def __init__(self):
        self.id = DiagramItem.__id
        DiagramItem.__id += 1

        self.parent: DiagramItem = None
        self.hover = False
        self.selected = False
        self.center = QPoint()
        self.movable: DragType = DragType.Movable

    def global_center(self):
        if self.parent is None:
            return self.center
        else:
            return self.center + self.parent.global_center()

    def get_id(self):
        return self.id

    def get_lines(self):
        return []

    def get_children(self) -> list:
        return []

    def point_hit_check(self, x, y) -> bool:
        return False

    def draw(self, qp: QPainter):
        pass




