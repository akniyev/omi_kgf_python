from PyQt5 import Qt
from PyQt5.Qt import *

from PyQt5.QtWidgets import QWidget


class DraggableWidget(QWidget):
    class Filter(QObject):
        def __init__(self):
            super().__init__()
            self.counter = 0

        def eventFilter(self, obj, event: QEvent):
            self.counter += 1
            # print("%s: FROM DRAGGABLE WIDGET: %s, is ACCEPTER: %s" % (self.counter, event.type(), event.isAccepted()))
            if event.type() == QEvent.MouseButtonPress:
                obj.mouse_press(event)
                return True
            elif event.type() == QEvent.MouseMove:
                obj.mouse_move(event)
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                obj.mouse_release(event)
                return True
            return False

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.can_drag = True
        self.drag_area: QRect = None
        self.setMouseTracking(True)
        self.position = QPoint(0, 0)
        self.cursor_position = QPointF(0, 0)
        self.setMouseTracking(True)
        self.is_dragging = False
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.filter = self.Filter()
        self.installEventFilter(self.filter)

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(QColor("yellow"))
        qp.fillRect(self.rect(), brush)
        qp.drawRect(self.rect())

        qp.end()

    def mouse_press(self, event: QMouseEvent):
        if self.can_drag and (self.drag_area is None or self.drag_area.contains(event.pos())):
            self.is_dragging = True
            self.position = self.pos()
            self.cursor_position = self.position + event.pos()
            # print("my_pos: {}".format(self.pos()))
            # print("curpos: {}".format(self.cursor_position))

    def mouse_move(self, event: QMouseEvent):
        if self.is_dragging and event.buttons() == Qt.LeftButton:
            delta: QPoint = self.pos() + event.windowPos() - self.cursor_position
            # print("delta: {}".format(delta))
            # print("curpos: {}".format(event.windowPos()))
            newpos = self.position + delta
            self.move(round(newpos.x()), round(newpos.y()))

    def mouse_release(self, event: QMouseEvent):
        self.is_dragging = False

    # def enterEvent(self, event: QEvent):
    #     print("enter")
    #
    # def leaveEvent(self, event: QEvent):
    #     print("leave")
