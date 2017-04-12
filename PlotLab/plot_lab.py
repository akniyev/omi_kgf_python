import textwrap
from enum import Enum
from random import randint

from PyQt5 import Qt
from abc import ABC, abstractmethod

import sys

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPaintEvent, QPainter, QMouseEvent, QColor, QPen, QBrush
from PyQt5.QtWidgets import *
from typing import List, Set, Dict


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


class DiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes: List[NodeInfo] = []
        self.setMouseTracking(True)
        self.selected_id = -1
        self.dragging = None
        for i in range(10):
            n = Node()
            n.set_arguments('x', 'y', 'z')
            n.set_results('a', 'b')
            ni = NodeInfo()
            ni.node = n
            ni.center = QPoint(randint(0, self.width()), randint(0, self.height()))

            self.nodes.append(ni)

    @staticmethod
    def draw_node(qp: QPainter, node_info: NodeInfo):
        background_color = node_info.get_background_color()
        border_color = node_info.get_border_color()
        border_width = node_info.get_border_width()
        node_rect = node_info.get_node_rect()
        pen = QPen(border_color)
        pen.setWidth(border_width)
        brush = QBrush()
        brush.setColor(background_color)
        brush.setStyle(1)

        qp.setPen(pen)
        qp.setBrush(brush)
        qp.fillRect(node_rect, brush)
        qp.drawRect(node_rect)

    def draw_nodes(self, qp: QPainter):
        if self.selected_id != -1:
            self.nodes[self.selected_id].state = NodeInfo.State.selected
        for ni in self.nodes:
            self.draw_node(qp, ni)

    def paintEvent(self, event : QPaintEvent):
        qp = QPainter()

        qp.begin(self)
        self.draw_nodes(qp)
        qp.end()

    def node_under_cursor(self, x, y):
        result = None
        for ni in self.nodes:
            if ni.point_over_node(x, y):
                result = ni
        return result

    def mouseMoveEvent(self, event: QMouseEvent):
        self.setWindowTitle("({}, {})".format(event.x(), event.y()))
        if self.dragging is None:
            for ni in self.nodes:
                ni.state = NodeInfo.State.normal
            ni = self.node_under_cursor(event.x(), event.y())
            if ni is not None:
                ni.state = NodeInfo.State.hover
        else:
            delta_x = event.x() - self.dragging[0]
            delta_y = event.y() - self.dragging[1]
            ni: NodeInfo = self.dragging[3]
            old_center: QPoint = self.dragging[2]
            ni.center = QPoint(old_center.x() + delta_x, old_center.y() + delta_y)
        self.repaint()

    def mousePressEvent(self, event: QMouseEvent):
        ni = self.node_under_cursor(event.x(), event.y())
        if ni is not None:
            self.dragging = (event.x(), event.y(), ni.center, ni)

    def mouseReleaseEvent(self, QMouseEvent):
        self.dragging = None
        self.repaint()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        ni = self.node_under_cursor(event.x(), event.y())
        self.selected_id = -1
        ns = self.nodes
        for i in range(len(self.nodes)):
            if ni == ns[i]:
                self.selected_id = i
                break
        self.repaint()


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
