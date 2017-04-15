from random import randint
from typing import List, Tuple

import math
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPaintEvent, QMouseEvent, QWheelEvent, QKeyEvent
from PyQt5.QtWidgets import QWidget, QPushButton

from PlotLab.Classes.Model.Node import Node
from PlotLab.Classes.View.NodeItem import NodeItem


class OldDiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes: List[NodeItem] = []
        self.setMouseTracking(True)
        self.selected_id = -1
        self.selected_handler_id = None
        self.dragging = None
        self.drag_coordinates = None
        self.lines = []  # (i1, node_info1, i2, node_info2)
        self.scale = 1
        self.offset = QPoint(0, 0)

        self.button = QPushButton("Press me!")
        self.button.setParent(self)

        for i in range(10):
            n = Node()
            n.set_arguments('x', 'y', 'z')
            n.set_results('a', 'b')
            ni = NodeItem()
            ni.node = n
            ni.center = QPoint(randint(0, self.width()), randint(0, self.height()))

            self.nodes.append(ni)

    def add_line(self, i1: int, node_info1: NodeItem, i2: int, node_info2: NodeItem):
        for line in self.lines:
            if line[2] == i2 and line[3] == node_info2:
                return
        self.lines.append((i1, node_info1, i2, node_info2))

    @staticmethod
    def line_magnitude(x1, y1, x2, y2):
        line_magnitude = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return line_magnitude

    # Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
    def distance_point_line(self, px, py, x1, y1, x2, y2):
        # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
        line_mag = self.line_magnitude(x1, y1, x2, y2)

        if line_mag < 0.00000001:
            distance_point_line = 9999
            return distance_point_line

        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (line_mag * line_mag)

        if (u < 0.00001) or (u > 1):
            # // closest point does not fall within the line segment, take the shorter distance
            # // to an endpoint
            ix = self.line_magnitude(px, py, x1, y1)
            iy = self.line_magnitude(px, py, x2, y2)
            if ix > iy:
                distance_point_line = iy
            else:
                distance_point_line = ix
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            distance_point_line = self.line_magnitude(px, py, ix, iy)

        return distance_point_line

    def draw_node(self, qp: QPainter, node_info: NodeItem):
        background_color = node_info.get_background_color()
        border_color = node_info.get_border_color()
        border_width = node_info.get_border_width()
        node_rect = node_info.get_node_rect()
        pen = QPen(border_color)
        pen.setWidth(border_width)
        brush = QBrush()
        brush.setColor(background_color)
        brush.setStyle(1)

        old_pen = qp.pen()
        old_brush = qp.brush()

        qp.setPen(pen)
        qp.setBrush(brush)
        qp.fillRect(node_rect, brush)
        qp.drawRect(node_rect)

        n_arg = len(node_info.node.arguments)
        for i in range(n_arg):
            rect = node_info.get_handle_rect(i, n_arg, -1)
            text_rect = node_info.get_handle_text_rect(i, n_arg, -1)
            pen = QPen(QColor(0, 0, 0))
            brush = QBrush(QColor(255, 255, 255), 1)

            if self.selected_handler_id is not None:
                if self.selected_handler_id[0] == 0:
                    handler_node = self.selected_handler_id[2]
                    if handler_node == node_info:
                        if self.selected_handler_id[1] == i:
                            pen.setWidth(node_info.border_width_selected)

            qp.setPen(pen)
            qp.setBrush(brush)

            qp.drawEllipse(rect)
            qp.drawText(text_rect, node_info.text_height, "x")

        pen = old_pen
        n_res = len(node_info.node.results)
        for i in range(n_res):
            rect = node_info.get_handle_rect(i, n_res, 1)
            text_rect = node_info.get_handle_text_rect(i, n_res, 1)

            pen = QPen(QColor(0, 0, 0))
            brush = QBrush(QColor(255, 255, 255), 1)

            if self.selected_handler_id is not None:
                if self.selected_handler_id[0] == 1:
                    handler_node = self.selected_handler_id[2]
                    if handler_node == node_info:
                        if self.selected_handler_id[1] == i:
                            pen.setWidth(node_info.border_width_selected)

            qp.setPen(pen)
            qp.setBrush(brush)

            qp.drawEllipse(rect)
            qp.drawText(text_rect, node_info.text_height, "a")
        qp.setPen(old_pen)
        qp.setBrush(old_brush)

    def draw_nodes(self, qp: QPainter):
        if self.selected_id != -1:
            self.nodes[self.selected_id].state = NodeItem.State.selected
        for ni in self.nodes:
            self.draw_node(qp, ni)
        self.draw_temporal_line(qp)
        self.draw_lines(qp)

    def draw_lines(self, qp: QPainter):
        for line in self.lines:
            (c1, c2) = self.get_line_coordinates(line)
            qp.drawLine(c1, c2)

    def draw_temporal_line(self, qp: QPainter):
        if self.dragging is not None:
            if self.dragging[0] == "line":
                if self.drag_coordinates is not None:
                    d = self.dragging[1]
                    position = d[0] * 2 - 1
                    i = d[1]
                    ni: NodeItem = d[2]
                    n = len(ni.node.arguments if position < 0 else ni.node.results)
                    c = ni.get_handle_center(i, n, position)
                    qp.drawLine(c.x(), c.y(), self.drag_coordinates[0], self.drag_coordinates[1])

    def get_line_coordinates(self, line) -> Tuple[QPoint, QPoint]:
        i1 = line[0]
        ni1: NodeItem = line[1]
        i2 = line[2]
        ni2: NodeItem = line[3]
        n1 = len(ni1.node.results)
        n2 = len(ni2.node.arguments)
        c1 = ni1.get_handle_center(i1, n1, 1)
        c2 = ni2.get_handle_center(i2, n2, -1)
        return (c1, c2)

    def line_under_cursor(self, x, y):
        selected_line_index = None
        for i in range(len(self.lines)):
            (c1, c2) = self.get_line_coordinates(self.lines[i])
            tol = 2
            if self.distance_point_line(x, y, c1.x(), c1.y(), c2.x(), c2.y()) < tol:
                selected_line_index = i
        return selected_line_index

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.scale(self.scale, self.scale)
        qp.translate(self.offset / self.scale)
        qp.setRenderHint(QPainter.Antialiasing)
        self.draw_nodes(qp)
        qp.end()

    def node_under_cursor(self, x, y):
        result = None
        for ni in self.nodes:
            if ni.point_over_node(x, y):
                result = ni
        return result

    def handler_under_cursor(self, x, y):
        handler_id = None
        for ni in self.nodes:
            handler_id = ni.point_over_handle(x, y)
            if handler_id is not None:
                return handler_id
        return None

    def mouseMoveEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        self.setWindowTitle("({}, {})".format(x, y))
        if self.dragging is None:
            for ni in self.nodes:
                ni.state = NodeItem.State.normal
            ni = self.node_under_cursor(x, y)
            if ni is not None:
                ni.state = NodeItem.State.hover
            handler_id = self.handler_under_cursor(x, y)
            self.selected_handler_id = handler_id
        elif self.dragging[0] == "drag":
            delta_x = x - self.dragging[1]
            delta_y = y - self.dragging[2]
            ni: NodeItem = self.dragging[4]
            old_center: QPoint = self.dragging[3]
            ni.center = QPoint(old_center.x() + delta_x, old_center.y() + delta_y)
        elif self.dragging[0] == "line":
            self.drag_coordinates = (x, y)
        elif self.dragging[0] == "plot":
            delta_x = event.x() - self.dragging[1]
            delta_y = event.y() - self.dragging[2]
            old_offset: QPoint = self.dragging[3]
            self.offset = QPoint(old_offset.x() + delta_x, old_offset.y() + delta_y)
            print("({}, {})".format(self.offset.x(), self.offset.y()))
        self.repaint()

    def wheelEvent(self, event: QWheelEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        delta_scale = 0.1

        if event.angleDelta().y() > 0:
            self.scale += delta_scale
        elif self.scale <= delta_scale * 2:
            return
        else:
            self.scale -= delta_scale

        delta_x = x * delta_scale
        delta_y = y * delta_scale

        if event.angleDelta().y() > 0:
            self.offset -= QPoint(delta_x, delta_y)
        else:
            self.offset += QPoint(delta_x, delta_y)

        self.repaint()

    def transform_mouse_coordinates(self, x, y):
        return (x - self.offset.x()) / self.scale, (y - self.offset.y()) / self.scale

    def mousePressEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        if event.button() == 1:
            ni = self.node_under_cursor(x, y)

            if ni is not None:
                self.dragging = ("drag", x, y, ni.center, ni)
            elif self.selected_handler_id is not None:
                if self.selected_handler_id[0] == 1:
                    self.dragging = ("line", self.selected_handler_id)
                    self.drag_coordinates = (x, y)
            else:
                self.dragging = ("plot", event.x(), event.y(), self.offset)
        elif event.button() == 2:
            selected_line = self.line_under_cursor(x, y)
            ni = self.node_under_cursor(x, y)
            self.selected_id = -1
            ns = self.nodes
            for i in range(len(self.nodes)):
                if ni == ns[i]:
                    self.selected_id = i
                    break
            if ni is None and selected_line is not None:
                del self.lines[selected_line]
        self.repaint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        if self.dragging is not None and self.dragging[0] == "line":
            release_handler = self.handler_under_cursor(x, y)
            if release_handler is not None:
                if self.selected_handler_id is not None:
                    if release_handler[0] == 0:
                        if release_handler[2] != self.dragging[1][2]:
                            so = self.selected_handler_id
                            de = release_handler
                            self.add_line(so[1], so[2], de[1], de[2])
                            print("Line drawn!")
        self.dragging = None
        self.repaint()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == 16777223:  # Delete key code = 32
            print("Delete pressed")