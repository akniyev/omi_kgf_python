from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPaintEvent, QPainter, QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QWidget

from PlotLab.Classes.View.DiagramItem import DiagramItem


class DiagramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__items = []

        # Viewport manipulation
        self.scale = 1
        self.offset = QPoint(0, 0)

        # Mouse interaction
        self.setMouseTracking(True)
        self.dragging = None

    def get_diagram_items(self) -> List[DiagramItem]:
        return self.__items

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
        qp.end()

    def draw_nodes(self, qp: QPainter):
        smeti = self.get_diagram_items()[:]
        smeti.reverse()
        for item in smeti:
            item.draw(qp)

    def get_first_item_under_cursor(self, x, y):
        for item in self.get_diagram_items():
            if item.point_hit_check(x, y):
                return item
        return None

    def mousePressEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        item = self.get_first_item_under_cursor(x ,y)
        if item is not None and item.movable:
            self.dragging = {"type": "item", "cursor": QPoint(x, y), "obj_center": item.center, "item": item}
        elif item is None:
            self.dragging = {"type": "scene", "cursor": QPoint(event.x(), event.y()), "obj_center": self.offset}
        # if event.button() == 1:
        #     ni = self.node_under_cursor(x, y)
        #
        #     if ni is not None:
        #         self.dragging = ("drag", x, y, ni.center, ni)
        #     elif self.selected_handler_id is not None:
        #         if self.selected_handler_id[0] == 1:
        #             self.dragging = ("line", self.selected_handler_id)
        #             self.drag_coordinates = (x, y)
        #     else:
        #         self.dragging = ("plot", event.x(), event.y(), self.offset)
        # elif event.button() == 2:
        #     selected_line = self.line_under_cursor(x, y)
        #     ni = self.node_under_cursor(x, y)
        #     self.selected_id = -1
        #     ns = self.nodes
        #     for i in range(len(self.nodes)):
        #         if ni == ns[i]:
        #             self.selected_id = i
        #             break
        #     if ni is None and selected_line is not None:
        #         del self.lines[selected_line]
        self.repaint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        self.dragging = None
        # if self.dragging is not None and self.dragging[0] == "line":
        #     release_handler = self.handler_under_cursor(x, y)
        #     if release_handler is not None:
        #         if self.selected_handler_id is not None:
        #             if release_handler[0] == 0:
        #                 if release_handler[2] != self.dragging[1][2]:
        #                     so = self.selected_handler_id
        #                     de = release_handler
        #                     self.add_line(so[1], so[2], de[1], de[2])
        #                     print("Line drawn!")
        # self.dragging = None
        self.repaint()

    def mouseMoveEvent(self, event: QMouseEvent):
        (x, y) = self.transform_mouse_coordinates(event.x(), event.y())
        if self.dragging is None:
            for item in self.get_diagram_items():
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
        # if self.dragging is None:
        #     for ni in self.nodes:
        #         ni.state = NodeItem.State.normal
        #     ni = self.node_under_cursor(x, y)
        #     if ni is not None:
        #         ni.state = NodeItem.State.hover
        #     handler_id = self.handler_under_cursor(x, y)
        #     self.selected_handler_id = handler_id
        # elif self.dragging[0] == "drag":
        #     delta_x = x - self.dragging[1]
        #     delta_y = y - self.dragging[2]
        #     ni: NodeItem = self.dragging[4]
        #     old_center: QPoint = self.dragging[3]
        #     ni.center = QPoint(old_center.x() + delta_x, old_center.y() + delta_y)
        # elif self.dragging[0] == "line":
        #     self.drag_coordinates = (x, y)
        # elif self.dragging[0] == "plot":
        #     delta_x = event.x() - self.dragging[1]
        #     delta_y = event.y() - self.dragging[2]
        #     old_offset: QPoint = self.dragging[3]
        #     self.offset = QPoint(old_offset.x() + delta_x, old_offset.y() + delta_y)
        #     print("({}, {})".format(self.offset.x(), self.offset.y()))
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