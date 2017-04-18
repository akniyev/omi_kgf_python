from typing import List

import math
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPaintEvent, QPainter, QMouseEvent, QWheelEvent, QColor, QPen, QKeyEvent
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import *

from PlotLab.Classes.View.DiagramItem import DiagramItem, DragType
from PlotLab.Classes.View.HandleItem import HandleItem, HandleType
from PlotLab.Classes.View.LineItem import LineItem
from PlotLab.Classes.View.NodeItem import NodeItem


class DiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__items = []

        # Viewport manipulation
        self.scale = 1
        self.offset = QPoint(0, 0)

        # Selection
        self.selected = set()

        # Mouse interaction
        self.setMouseTracking(True)
        self.dragging = None
        self.cursor_position = QPoint()
        self.last_press_cursor_position = QPoint()
        self.ctrl_pressed = False

        from PlotLab.Classes.View import NodeSettingsWidget
        self.settings_widget: NodeSettingsWidget = None

    def get_all_diagram_items(self) -> List[DiagramItem]:
        result = []
        for item in self.__items:
            result.append(item)
            result.extend(item.get_children())
        return result

    def add_diagram_item(self, item: DiagramItem):
        self.__items.append(item)
        self.repaint()

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.scale(self.scale, self.scale)
        qp.translate(self.offset / self.scale)
        qp.setRenderHint(QPainter.Antialiasing)
        self.draw_nodes(qp)
        self.draw_drag_line(qp)
        self.draw_lines(qp)

        qp.end()

    def draw_lines(self, qp: QPainter):
        lines = self.get_all_lines()
        for line in lines:
            line.draw(qp)

    def draw_drag_line(self, qp: QPainter):
        if self.dragging is not None:
            if self.dragging["type"] == "line":
                s: DiagramItem = self.dragging["source"]
                start_point = s.global_center()
                end_point = self.cursor_position
                pen = QPen(QColor("green"))
                pen.setWidth(2)
                qp.setPen(pen)
                qp.drawLine(start_point, end_point)

    def get_all_lines(self) -> List[LineItem]:
        result = set()
        for i in self.get_all_diagram_items():
            result = result.union(i.get_lines())
        return result

    def draw_nodes(self, qp: QPainter):
        smeti = self.get_all_diagram_items()[:]
        smeti.reverse()
        for item in smeti:
            item.draw(qp)

    def select_deselect(self, item: DiagramItem, ctrl = False):
        if type(item) == NodeItem or type(item) == LineItem:
            if item in self.selected:
                if ctrl:
                    self.selected.remove(item)
                else:
                    self.selected = set([item])
            else:
                if ctrl:
                    self.selected.add(item)
                else:
                    self.selected = set([item])
        elif item is None:
            self.selected = set()
        self.apply_selection()

    def apply_selection(self):
        items = self.get_all_diagram_items()
        for item in items:
            if type(item) == NodeItem or type(item) == LineItem:
                item.selected = item in self.selected
        items = self.get_all_lines()
        for item in items:
            if type(item) == NodeItem or type(item) == LineItem:
                item.selected = item in self.selected
        self.reload_graph()

    @staticmethod
    def connect_with_line(h1: HandleItem, h2: HandleItem):
        if h1.type == HandleType.Input and h2.type == HandleType.Output:
            h = h1
            h1 = h2
            h2 = h
        elif h1.type != HandleType.Output or h2.type != HandleType.Input:
            return
        line = LineItem()
        line.set_ends(h1, h2)

    def get_first_item_under_cursor(self, x, y):
        for item in self.get_all_diagram_items():
            if item.point_hit_check(x, y):
                return item
        for item in self.get_all_lines():
            if item.point_hit_check(x, y):
                return item
        return None

    def mousePressEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        self.last_press_cursor_position = QPoint(x, y)
        item = self.get_first_item_under_cursor(x ,y)
        if item is not None and item.movable == DragType.Movable:
            self.dragging = {"type": "item", "cursor": QPoint(x, y), "obj_center": item.center, "item": item}
        elif item is not None and item.movable == DragType.Line:
            self.dragging = {"type": "line", "source": item}
        elif item is None:
            self.dragging = {"type": "scene", "cursor": QPoint(event.x(), event.y()), "obj_center": self.offset}
        self.repaint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        if self.dragging is not None and self.dragging["type"] == "line":
            dest_item = self.get_first_item_under_cursor(x, y)
            if dest_item is not None and type(dest_item) == HandleItem:
                self.connect_with_line(self.dragging["source"], dest_item)
        elif math.fabs(self.last_press_cursor_position.x() - x) < 1 and math.fabs(self.last_press_cursor_position.y() - y) < 1:
            if self.dragging is not None and self.dragging["type"] == "scene":
                old_cursor_pos = self.dragging["cursor"]
                new_cursor_pos = event.pos()
                diff: QPoint = (old_cursor_pos - new_cursor_pos)
                if diff.x() ** 2 + diff.y() ** 2 <= 2:
                    self.select_deselect(self.get_first_item_under_cursor(x, y), self.ctrl_pressed)
            else:
                self.select_deselect(self.get_first_item_under_cursor(x, y), self.ctrl_pressed)
        self.dragging = None
        self.repaint()

    def mouseMoveEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        self.cursor_position = QPoint(x, y)
        if self.dragging is None:
            for item in self.get_all_diagram_items():
                item.hover = False
            for item in self.get_all_lines():
                item.hover = False
            hover_item = self.get_first_item_under_cursor(x, y)
            if hover_item is not None:
                hover_item.hover = True
        elif self.dragging["type"] == "item":
            delta_x = x - self.dragging["cursor"].x()
            delta_y = y - self.dragging["cursor"].y()
            item = self.dragging["item"]
            old_center: QPoint = self.dragging["obj_center"]
            item.center = QPoint(old_center.x() + delta_x, old_center.y() + delta_y)
        elif self.dragging["type"] == "scene":
            delta_x = event.x() - self.dragging["cursor"].x()
            delta_y = event.y() - self.dragging["cursor"].y()
            old_offset: QPoint = self.dragging["obj_center"]
            self.offset = QPoint(old_offset.x() + delta_x, old_offset.y() + delta_y)
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

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        item = self.get_first_item_under_cursor(x, y)
        if item is not None and type(item) == NodeItem:
            self.open_settings(item)
        elif item is not None and type(item) == HandleItem:
            if item.type == HandleType.Output:
                print("VALUE: %s" % item.out_value)

    def open_settings(self, node: NodeItem):
        if self.settings_widget is not None:
            self.settings_widget.load_node(node, self)

    def transform_mouse_coordinates(self, x, y):
        return (x - self.offset.x()) / self.scale, (y - self.offset.y()) / self.scale

    # Keyboard interaction
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = True

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.delete_selected()
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False

    # Add/Delete items
    def delete_line(self, line: LineItem, repaint=True):
        line.remove()
        if repaint:
            self.repaint()

    def delete_node(self, node: NodeItem, repaint=True):
        node_lines = node.get_lines()
        for line in node_lines:
            self.delete_line(line)
        if node in self.__items:
            self.__items.remove(node)
        if repaint:
            self.repaint()

    def delete_selected(self):
        for item in list(self.selected):
            self.selected.remove(item)
            if item is not None:
                if type(item) == NodeItem:
                    self.delete_node(item, False)
                elif type(item) == LineItem:
                    self.delete_line(item, False)
        self.repaint()

    def reload_graph(self):
        self.repaint()

    # Calculating
    def calculated_inputs_nodes(self):
        result = []
        for node in self.__items:
            if type(node) == NodeItem:
                if node.is_ready_to_compute() and not node.is_result_computed():
                    result.append(node)
        return result

    def calculate_iteration(self):
        nodes_to_calculate = self.calculated_inputs_nodes()
        print(len(nodes_to_calculate))
        for node in nodes_to_calculate:
            node.compute()
