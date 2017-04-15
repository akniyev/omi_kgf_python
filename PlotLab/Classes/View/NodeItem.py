from typing import List

from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.Qt import *

from PlotLab.Classes.Model.Node import Node
from PlotLab.Classes.Model.NodeArgument import NodeArgument
from PlotLab.Classes.Model.NodeResult import NodeResult
from PlotLab.Classes.View.HandleItem import HandleItem
from PlotLab.Classes.View.DiagramItem import DiagramItem


class NodeItem(DiagramItem):
    def __init__(self):
        super().__init__()
        self.node: Node = Node()
        self.input_handlers: List[HandleItem] = []
        self.output_handlers: List[HandleItem] = []
        self.size = QSize(50, 50)
        self.handle_radius = 5

    def get_global_rect(self):
        c = self.global_center()
        s = self.size
        return QRect(c.x() - s.width() / 2 + self.handle_radius * 2, c.y() - s.height() / 2, s.width() - 2 * self.handle_radius * 2, s.height())

    def point_hit_check(self, x, y):
        return self.get_global_rect().contains(x, y)

    def get_children(self):
        return self.input_handlers + self.output_handlers

    def draw(self, qp: QPainter):
        rect = self.get_global_rect()
        qp.drawRect(rect)
        brush = QBrush()
        brush.setColor(QColor("green"))
        brush.setStyle(Qt.SolidPattern)
        qp.fillRect(rect, brush)
        for i in self.input_handlers:
            i.draw(qp)
        for o in self.output_handlers:
            o.draw(qp)

    def set_node_inputs(self, *inputs):

        self.node.set_arguments(*list(inputs))
        self.rebuild_handles()

    def set_node_outputs(self, *outputs):
        self.node.set_results(*list(outputs))
        self.rebuild_handles()

    def add_node_input(self, input_name):
        self.node.add_argument(input_name)
        self.rebuild_handles()

    def add_node_output(self, output_name):
        self.node.add_result(output_name)
        self.rebuild_handles()

    def rebuild_handles(self):
        self.input_handlers: List[HandleItem] = []
        self.output_handlers: List[HandleItem] = []
        for input in self.node.arguments:
            ihandle = HandleItem()
            ihandle.name = input
            ihandle.radius = self.handle_radius
            ihandle.parent = self
            self.input_handlers.append(ihandle)
        for output in self.node.results:
            ohandle = HandleItem()
            ohandle.name = output
            ohandle.radius = self.handle_radius
            ohandle.parent = self
            self.output_handlers.append(ohandle)
        iN = len(self.input_handlers)
        for i in range(iN):
            s = self.size
            cx = - (s.width() / 2 - self.handle_radius / 2)
            cy = - s.height() / 2 + s.height() / iN * (i + 0.5)
            self.input_handlers[i].center = QPoint(cx, cy)
        oN = len(self.output_handlers)
        for i in range(oN):
            s = self.size
            cx = (s.width() / 2 - self.handle_radius / 2)
            cy = - s.height() / 2 + s.height() / oN * (i + 0.5)
            self.output_handlers[i].center = QPoint(cx, cy)



