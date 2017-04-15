from enum import Enum
from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter


class DiagramItem:
    def __init__(self):
        self.hover = False
        self.selected = False
        self.movable = True
        self.children: List[DiagramItem] = []

    def point_hit_check(self, x, y) -> bool:
        return False

    def draw(self, qp: QPainter):
        pass




