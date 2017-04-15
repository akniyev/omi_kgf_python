from enum import Enum

from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QColor

from PlotLab.Classes.Model.Node import Node


class NodeItem:
    class State(Enum):
        normal = 0
        selected = 1
        hover = 2

    def __init__(self):
        super().__init__()
        self.node: Node = None
        self.center: QPoint = QPoint(0, 0)
        self.width = 100
        self.height = 100
        self.state = self.State.normal

        self.border_color = QColor(0, 0, 0)
        self.border_color_selected = QColor(255, 201, 14)
        self.border_color_hover = QColor(255, 237, 174)
        self.border_width = 1
        self.border_width_hover = 3
        self.border_width_selected = 3
        self.background_color = QColor(200, 200, 200)
        self.background_color_selected = QColor(200, 200, 250)
        self.background_color_hover = QColor(230, 230, 230)

        self.handler_radius = 5
        self.text_height = 10

    def get_background_color(self):
        if self.state == self.State.normal:
            return self.background_color
        elif self.state == self.State.hover:
            return self.background_color_hover
        else:
            return self.background_color_selected

    def get_border_color(self):
        if self.state == self.State.normal:
            return self.border_color
        elif self.state == self.State.hover:
            return self.border_color_hover
        else:
            return self.border_color_selected

    def get_border_width(self):
        if self.state == self.State.normal:
            return self.border_width
        elif self.state == self.State.hover:
            return self.border_width_hover
        else:
            return self.border_width_selected

    def get_node_rect(self) -> QRect:
        c = self.center
        w = self.width
        h = self.height
        return QRect(c.x() - w / 2, c.y() - h / 2, w, h)

    def point_over_node(self, x, y):
        rect = self.get_node_rect()
        return rect.contains(x, y)

    def get_handle_center(self, i, n, position):
        dist_from_edge = 5
        center_y = (self.center.y() - self.height / 2) + (i + 0.5) * (self.height / n)
        center_x = self.center.x() + position * (self.width / 2 + dist_from_edge)
        return QPoint(center_x, center_y)

    def get_handle_rect(self, i, n, position): # i: number of handle, n: total number of handlers, position: 1 or -1 (left, right)
        center = self.get_handle_center(i, n, position)
        radius = self.handler_radius
        return QRect(center.x() - radius, center.y() - radius, radius * 2, radius * 2)

    def get_handle_text_rect(self, i, n, position): # i: number of handle, n: total number of handlers, position: 1 or -1 (left, right)
        center_y = (self.center.y() - self.height / 2) + (i + 0.5) * (self.height / n)
        radius = self.text_height
        center_x = self.center.x() + self.width / 2 - radius if position == 1 else self.center.x() - self.width / 2

        return QRect(center_x - radius, center_y - radius, radius * 2, radius * 2)

    def point_over_handle(self, x, y):
        n = len(self.node.arguments)
        for i in range(n):
            if self.get_handle_rect(i, n, -1).contains(QPoint(x, y)):
                return 0, i, self

        n = len(self.node.results)
        for i in range(n):
            if self.get_handle_rect(i, n, 1).contains(QPoint(x, y)):
                return 1, i, self
        return None