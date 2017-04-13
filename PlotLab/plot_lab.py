import textwrap
from enum import Enum
from random import randint

from PyQt5 import Qt
from abc import ABC, abstractmethod

import sys

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPaintEvent, QPainter, QMouseEvent, QColor, QPen, QBrush, QKeyEvent, QWheelEvent
from PyQt5.QtWidgets import *
from typing import List, Set, Dict, Tuple

from numpy import arccos, array, dot, pi
from numpy.linalg import det, norm

import math


# Model
class NodeArgument:
    def __init__(self):
        self.name: str = None
        self.node: Node = None
        self.in_value: NodeResult = None


class NodeResult:
    def __init__(self):
        self.name: str = None
        self.node: Node = None
        self.value = None
        self.targets: Set[NodeArgument] = set()


class Function:
    # CLASS:
    # @staticmethod
    # class NodeFunction:
    #     def compute_values(self, values):
    #         pass

    def __init__(self):
        self.counter = 0
        self.function_name = ""
        self.function_body = ""

    def get_next_counter(self):
        self.counter += 1
        return self.counter

    def compute(self, arguments: List[NodeArgument], results: List[NodeResult]):
        num = self.get_next_counter()
        fun_name = "Node{}{}".format(self.function_name, num)
        body = textwrap.indent(self.function_body, "  ")
        body = "class {}:\n".format(fun_name) + body
        values = {}
        for argument in arguments:
            values[argument.name] = argument.in_value.value
        f_call = "{}.compute_values(values)".format(fun_name)
        exec(body)
        computed_result = eval(f_call)
        for node_result in results:
            if node_result.name not in computed_result:
                return False

        for node_result in results:
            node_result.value = computed_result[node_result.name]

        return True


class Node:
    def __init__(self):
        self.id: int = None
        self.arguments: Dict[str, NodeArgument] = {}  # {name : InputConnection}
        self.results: Dict[str, NodeResult] = {}  # {name : OutputConnection}

        self.function: Function = None  # Function
        self.display_function: Function = None  # Function
        self.import_modules: List[str] = []  # [String], example: ['import numpy as np']

    def can_compute(self):
        for arg in self.arguments.values():
            if arg.in_value.value is None:
                return False
        if self.function is None:
            return False
        return True

    def get_argument(self, name: str):
        if name in self.arguments.keys():
            return self.arguments[name]
        else:
            return None

    def get_result(self, name: str):
        if name in self.results.keys():
            return self.results[name]
        else:
            return None

    def add_argument(self, name):
        if name not in self.arguments.keys():
            na = NodeArgument()
            na.name = name
            na.node = self
            self.arguments[name] = na
        else:
            print('Element with name {} already exists!'.format(name))

    def remove_argument(self, name):
        if name in self.arguments:
            arg: NodeArgument = self.arguments[name]
            if arg.in_value is not None:
                if arg in arg.in_value.targets:
                    arg.in_value.targets.remove(arg)
            del self.arguments[name]
        else:
            print('No element with name {}'.format(name))

    def add_result(self, name):
        if name not in self.results.keys():
            nr = NodeResult()
            nr.name = name
            nr.node = self
            self.results[name] = nr

    def remove_result(self, name):
        if name in self.results.keys():
            res: NodeResult = self.results[name]
            for target in res.targets:
                target.in_value = None
            del self.results[name]
        else:
            print('No element with name {}'.format(name))

    def set_arguments(self, *names):
        arg_names = list(self.arguments.keys())
        for name in arg_names:
            if name not in names:
                self.remove_argument(name)

        for name in names:
            if self.get_argument(name) is None:
                self.add_argument(name)

    def set_results(self, *names):
        res_names = list(self.results.keys())
        for name in res_names:
            if name not in names:
                self.remove_result(name)

        for name in names:
            if self.get_result(name) is None:
                self.add_result(name)

    def compute(self):
        if not self.can_compute():
            return False

        self.function.compute(list(self.arguments.values()), list(self.results.values()))
        return True

    @staticmethod
    def connect(result: NodeResult, argument: NodeArgument):
        if argument.in_value is None:
            argument.in_value = result
            result.targets.add(argument)

    @staticmethod
    def disconnect(result: NodeResult, argument: NodeArgument):
        if argument.in_value == result and argument in result.targets:
            argument.in_value = None
            if argument in result.targets:
                result.targets.remove(argument)


class ConstantFunction(Function):
    def __init__(self, value, name: str):
        super().__init__()
        self.function_body = ("@staticmethod\n"
                              "def compute_values(values):\n"
                              "  return {'a': 2}")
        self.function_name = name


class SimpleFunction(Function):
    def __init__(self, expressions: Dict[str, str], name: str): # SimpleFunction({'b': 'x * x * x'}, "Simplefunction")
        super().__init__()
        self.function_name = name
        self.function_body = expressions

    def compute(self, arguments: List[NodeArgument], results: List[NodeResult]):
        values = {}
        expressions: Dict[str, str] = self.function_body
        for argument in arguments:
            values[argument.name] = argument.in_value.value
        computed_result = {}
        for arg_name in expressions.keys():
            arg_value = eval(expressions[arg_name], values)
            computed_result[arg_name] = arg_value
        for node_result in results:
            node_result.value = computed_result[node_result.name]

        return True


class NodeInfo:
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


class DiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes: List[NodeInfo] = []
        self.setMouseTracking(True)
        self.selected_id = -1
        self.selected_handler_id = None
        self.dragging = None
        self.drag_coordinates = None
        self.lines = []  # (i1, node_info1, i2, node_info2)
        self.scale = 1
        self.offset = QPoint(0, 0)

        for i in range(10):
            n = Node()
            n.set_arguments('x', 'y', 'z')
            n.set_results('a', 'b')
            ni = NodeInfo()
            ni.node = n
            ni.center = QPoint(randint(0, self.width()), randint(0, self.height()))

            self.nodes.append(ni)

    def add_line(self, i1: int, node_info1: NodeInfo, i2: int, node_info2: NodeInfo):
        for line in self.lines:
            if line[2] == i2 and line[3] == node_info2:
                return
        self.lines.append((i1, node_info1, i2, node_info2))

    def lineMagnitude(self, x1, y1, x2, y2):
        lineMagnitude = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return lineMagnitude

    # Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
    def DistancePointLine(self, px, py, x1, y1, x2, y2):
        # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
        LineMag = self.lineMagnitude(x1, y1, x2, y2)

        if LineMag < 0.00000001:
            DistancePointLine = 9999
            return DistancePointLine

        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (LineMag * LineMag)

        if (u < 0.00001) or (u > 1):
            # // closest point does not fall within the line segment, take the shorter distance
            # // to an endpoint
            ix = self.lineMagnitude(px, py, x1, y1)
            iy = self.lineMagnitude(px, py, x2, y2)
            if ix > iy:
                DistancePointLine = iy
            else:
                DistancePointLine = ix
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            DistancePointLine = self.lineMagnitude(px, py, ix, iy)

        return DistancePointLine

    def draw_node(self, qp: QPainter, node_info: NodeInfo):
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
            self.nodes[self.selected_id].state = NodeInfo.State.selected
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
                    ni: NodeInfo = d[2]
                    n = len(ni.node.arguments if position < 0 else ni.node.results)
                    c = ni.get_handle_center(i, n, position)
                    qp.drawLine(c.x(), c.y(), self.drag_coordinates[0], self.drag_coordinates[1])

    def get_line_coordinates(self, line) -> Tuple[QPoint, QPoint]:
        i1 = line[0]
        ni1: NodeInfo = line[1]
        i2 = line[2]
        ni2: NodeInfo = line[3]
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
            if self.DistancePointLine(x, y, c1.x(), c1.y(), c2.x(), c2.y()) < tol:
                selected_line_index = i
        return selected_line_index


    def paintEvent(self, event: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.scale(self.scale, self.scale)
        qp.translate(self.offset / self.scale)
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
                ni.state = NodeInfo.State.normal
            ni = self.node_under_cursor(x, y)
            if ni is not None:
                ni.state = NodeInfo.State.hover
            handler_id = self.handler_under_cursor(x, y)
            self.selected_handler_id = handler_id
        elif self.dragging[0] == "drag":
            delta_x = x - self.dragging[1]
            delta_y = y - self.dragging[2]
            ni: NodeInfo = self.dragging[4]
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
            selected_line = self.line_under_cursor(event.x(), event.y())
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


if __name__ == "__main__":
    n1 = Node()
    n2 = Node()
    n1.add_result('a')
    n2.add_argument('x')
    n2.add_argument('y')
    Node.connect(n1.get_result('a'), n2.get_argument('x'))
    Node.connect(n1.get_result('a'), n2.get_argument('y'))
    # Node.disconnect(n1.get_result('a'), n2.get_argument('x'))
    n1.set_results('a', 'b', 'c')
    n2.set_arguments('x', 'z')
    n3 = Node()
    n3.set_results('a')

    n3.function = ConstantFunction(2, "Constant2")

    n4 = Node()
    n4.set_arguments('x')
    n4.set_results('b')
    f2 = Function()
    f2.function_name = "Square"
    f2.function_body = """@staticmethod
def compute_values(values):
    x = values['x']
    return { 'b' : x * x }
"""
    n4.function = SimpleFunction({'b': 'x * x * x'}, "Simplefunction")
    Node.connect(n3.get_result('a'), n4.get_argument('x'))
    n3.compute()
    n4.compute()
    # @staticmethod
    # class NodeFunction:
    #     def compute_values(values):
    #         pass

    app = QApplication(sys.argv)

    node_widget = DiagramWidget()
    node_widget.show()

    sys.exit(app.exec_())
