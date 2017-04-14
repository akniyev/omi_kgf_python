from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView


class SchemeWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scale_ratio = 1
        self.canvas_offset = QPoint()
        self.setRenderHint(QPainter.Antialiasing)

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y() / 120 / 10
        self.scale_ratio += delta
        self.resetTransform()
        self.scale(self.scale_ratio, self.scale_ratio)


