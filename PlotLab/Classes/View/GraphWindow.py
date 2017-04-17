from random import randint

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt5.Qt import *

from PlotLab.Classes.View.DiagramWidget import DiagramWidget
from PlotLab.Classes.View.NodeItem import NodeItem
from PlotLab.Classes.View.NodeSettingsWidget import NodeSettingsWidget


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.diagram_widget = DiagramWidget()
        self.settings_widget = NodeSettingsWidget()
        self.diagram_widget.settings_widget = self.settings_widget
        self.settings_widget.setFixedWidth(350)
        self.diagram_widget.setFocusPolicy(Qt.ClickFocus)

        self.hbox_buttons = QHBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.diagram_widget)
        self.hbox.addWidget(self.settings_widget)

        self.add_button = QPushButton("Add node")
        self.add_button.setFixedWidth(90)
        self.add_const_button = QPushButton("Add const")
        self.add_const_button.setFixedWidth(90)
        self.calculate_button = QPushButton("One iteration")
        self.calculate_button.setFixedWidth(90)
        self.hbox_buttons.addWidget(self.add_button)
        self.hbox_buttons.addWidget(self.calculate_button)
        self.hbox_buttons.addWidget(self.add_const_button)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox_buttons)

        self.setLayout(self.vbox)

        self.add_button.clicked.connect(self.add_node)
        self.calculate_button.clicked.connect(self.calculate)
        self.add_const_button.clicked.connect(self.add_constant_node)

    def add_node(self):
        ni = NodeItem()
        ni.center = QPoint(randint(1, 400), randint(1, 400))
        ni.set_node_inputs(['x', 'y'])
        ni.set_node_outputs(['a', 'b'])
        self.diagram_widget.add_diagram_item(ni)

    def add_constant_node(self):
        ni = NodeItem()
        ni.center = QPoint(randint(1, 400), randint(1, 400))
        ni.set_node_outputs(['a'])
        ni.function_body = ("@staticmethod\n"
                            "def compute_values(values):\n"
                            "  %VALUES%\n"
                            "  a = 1\n"
                            "  %RETURN%\n")
        self.diagram_widget.add_diagram_item(ni)

    def calculate(self):
        self.diagram_widget.calculate_iteration()
        self.diagram_widget.reload_graph()