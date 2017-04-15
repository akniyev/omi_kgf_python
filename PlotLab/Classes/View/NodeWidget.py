from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QGridLayout

from PlotLab.Classes.Model.Node import Node
from PlotLab.Classes.View.DraggableWidget import DraggableWidget


class NodeWidget(DraggableWidget):
    def __init__(self):
        super().__init__()


        self.setGeometry(0, 0, 25, 50)

        self.drag_area = QRect(5, 0, 15, 50)
        self.input_handle_widget = []
        self.output_handle_widget = []
        self.setNode(Node())


    def setNode(self, node):
        self.node = node