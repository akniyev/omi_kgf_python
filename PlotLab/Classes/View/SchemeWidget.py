from PyQt5.QtCore import QPoint, Qt, QObject, QEvent
from PyQt5.QtGui import QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget


class SchemeWidget(QGraphicsView):
    class Filter(QObject):
        def __init__(self):
            super().__init__()

        def eventFilter(self, obj, event: QEvent):
            if event.type() == QEvent.MouseButtonPress:
                print("press")
                return True
            elif event.type() == QEvent.MouseMove:
                o: SchemeWidget = obj.parent()
                o.mouse_move(event)
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                print("release")
                return True
            return False

    def __init__(self):
        super().__init__()
        self.scale_ratio = 1
        s = QGraphicsScene()
        s.setSceneRect(-500, -500, 1000, 1000)
        self.setScene(s)
        self.canvas_offset = QPoint()
        self.setRenderHint(QPainter.Antialiasing)
        # self.filter = self.Filter()
        # self.viewport().installEventFilter(self.filter)


