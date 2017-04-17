from typing import List

from PyQt5.QtCore import QSize, QPoint, QRect
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.Qt import *

from PlotLab.Classes.Model.Node import Node
from PlotLab.Classes.Model.NodeArgument import NodeArgument
from PlotLab.Classes.Model.NodeResult import NodeResult
from PlotLab.Classes.View.HandleItem import HandleItem, HandleType
from PlotLab.Classes.View.DiagramItem import DiagramItem


class NodeItem(DiagramItem):
    def __init__(self):
        super().__init__()
        self.node: Node = Node()
        self.name = "Node"
        self.input_handlers: List[HandleItem] = []
        self.output_handlers: List[HandleItem] = []
        self.size = QSize(70, 50)
        self.handle_radius = 5
        self.text_height = 15
        self.function_body = ("@staticmethod\n"
                              "def compute_values(self, values):\n"
                              "  pass\n")


    def get_global_rect(self):
        c = self.global_center()
        s = self.size
        return QRect(c.x() - s.width() / 2 + self.handle_radius * 2, c.y() - s.height() / 2, s.width() - 2 * self.handle_radius * 2, s.height())

    def point_hit_check(self, x, y):
        return self.get_global_rect().contains(x, y)

    def get_children(self):
        return self.input_handlers + self.output_handlers

    def get_lines(self):
        result = set()
        for line in self.input_handlers + self.output_handlers:
            lines = line.get_lines()
            result = result.union(set(lines))
        return list(result)

    def draw(self, qp: QPainter):
        rect = self.get_global_rect()
        brush = QBrush()
        brush.setColor(QColor("white") if not self.selected else QColor(100, 100, 200))
        brush.setStyle(Qt.SolidPattern)
        qp.fillRect(rect, brush)
        pen = QPen(QColor("black"))
        pen.setWidth(3 if self.hover else 1)
        qp.setPen(pen)
        qp.drawRect(rect)
        for i in self.input_handlers:
            i.draw(qp)
        for o in self.output_handlers:
            o.draw(qp)
        qp.drawText(self.get_text_rect(), 5, self.name)

    def get_text_rect(self):
        c = self.global_center()
        return QRect(c.x() - self.size.width() / 2 + self.handle_radius, c.y() - self.text_height / 2, self.size.width() - self.handle_radius * 2, self.text_height)

    def set_node_inputs(self, inputs: List[str]):
        old_inputs = list(map(lambda x: x.name, self.input_handlers))
        inputs_to_delete = []
        inputs_to_add = []
        for new_input_name in inputs:
            if new_input_name not in old_inputs:
                inputs_to_add.append(new_input_name)
        for old_name in old_inputs:
            if old_name not in inputs:
                inputs_to_delete.append(old_name)
        for input_name in inputs_to_add:
            self.add_node_input(input_name)
        for input_name in inputs_to_delete:
            self.delete_node_input(input_name)

    def set_node_outputs(self, outputs: List[str]):
        old_outputs = list(map(lambda x: x.name, self.output_handlers))
        outputs_to_delete = []
        outputs_to_add = []
        for new_output_name in outputs:
            if new_output_name not in old_outputs:
                outputs_to_add.append(new_output_name)
        for old_name in old_outputs:
            if old_name not in outputs:
                outputs_to_delete.append(old_name)
        for output_name in outputs_to_add:
            self.add_node_output(output_name)
        for output_name in outputs_to_delete:
            self.delete_node_output(output_name)

    def add_node_input(self, input_name):
        item = HandleItem()
        item.name = input_name
        item.type = HandleType.Input
        item.radius = self.handle_radius
        item.parent = self
        self.input_handlers.append(item)
        self.order_handlers()

    def add_node_output(self, output_name):
        item = HandleItem()
        item.name = output_name
        item.type = HandleType.Output
        item.radius = self.handle_radius
        item.parent = self
        self.output_handlers.append(item)
        self.order_handlers()

    def delete_node_input(self, input_name):
        item = None
        for i in self.input_handlers:
            if i.name == input_name:
                item = i
                break
        if item is not None:
            if item.input_line is not None:
                item.input_line.remove()
            for ol in list(item.output_lines):
                ol.remove()
            self.input_handlers.remove(item)
        self.order_handlers()

    def delete_node_output(self, output_name):
        item = None
        for i in self.output_handlers:
            if i.name == output_name:
                item = i
                break
        if item is not None:
            if item.input_line is not None:
                item.input_line.remove()
            for ol in list(item.output_lines):
                ol.remove()
            self.output_handlers.remove(item)
        self.order_handlers()

    def order_handlers(self):
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

    def rebuild_handles(self):
        self.input_handlers: List[HandleItem] = []
        self.output_handlers: List[HandleItem] = []
        for input in self.node.arguments:
            ihandle = HandleItem()
            ihandle.name = input
            ihandle.type = HandleType.Input
            ihandle.radius = self.handle_radius
            ihandle.parent = self
            self.input_handlers.append(ihandle)
        for output in self.node.results:
            ohandle = HandleItem()
            ohandle.name = output
            ohandle.type = HandleType.Output
            ohandle.radius = self.handle_radius
            ohandle.parent = self
            self.output_handlers.append(ohandle)




