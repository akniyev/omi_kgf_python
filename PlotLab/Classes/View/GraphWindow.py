from random import randint

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt5.Qt import *

from PlotLab.Classes.View.DiagramWidget import DiagramWidget
from PlotLab.Classes.View.NodeItem import NodeItem
from PlotLab.Classes.View.NodeSettingsWidget import NodeSettingsWidget
from PlotLab.Classes.View.PlotItem2d import PlotItem2d
from PlotLab.Classes.View.Widgets.PlotsWidget import PlotsWidget


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.diagram_widget = DiagramWidget()
        self.settings_widget = NodeSettingsWidget()
        self.diagram_widget.settings_widget = self.settings_widget
        self.settings_widget.setFixedWidth(350)
        self.diagram_widget.setFocusPolicy(Qt.ClickFocus)

        self.plots_widget = PlotsWidget()
        self.diagram_widget.plots_widget = self.plots_widget
        self.plots_widget.setGeometry(10, 10, 800, 500)
        self.plots_widget.show()

        self.hbox_buttons = QHBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.diagram_widget)
        self.hbox.addWidget(self.settings_widget)

        self.add_button = QPushButton("Add node")
        self.add_button.setFixedWidth(90)
        self.add_2d_plot_button = QPushButton("Add plot2d")
        self.add_2d_plot_button.setFixedWidth(90)
        self.add_const_button = QPushButton("Add const")
        self.add_const_button.setFixedWidth(90)
        self.add_const_array_button = QPushButton("Add const array")
        self.add_const_array_button.setFixedWidth(90)
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFixedWidth(90)
        self.hbox_buttons.addWidget(self.add_button)
        self.hbox_buttons.addWidget(self.calculate_button)
        self.hbox_buttons.addWidget(self.add_const_button)
        self.hbox_buttons.addWidget(self.add_const_array_button)
        self.hbox_buttons.addWidget(self.add_2d_plot_button)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox_buttons)

        self.setLayout(self.vbox)

        self.add_button.clicked.connect(self.add_node)
        self.calculate_button.clicked.connect(self.calculate)
        self.add_const_button.clicked.connect(self.add_constant_node)
        self.add_2d_plot_button.clicked.connect(self.add_2d_plot_node)
        self.add_const_array_button.clicked.connect(self.add_constant_array_node)

    def add_node(self):
        ni = NodeItem()
        ni.center = QPoint(randint(1, 400), randint(1, 400))
        ni.set_node_inputs(['x', 'y'])
        ni.set_node_outputs(['a', 'b'])
        ni.function_body = ("@staticmethod\n"
                            "def compute_values(values):\n"
                            "  %VALUES%\n"
                            "  a = x\n"
                            "  b = y\n"
                            "  %RETURN%\n")
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

    def add_constant_array_node(self):
        ni = NodeItem()
        ni.center = QPoint(randint(1, 400), randint(1, 400))
        ni.set_node_outputs(['a'])
        ni.function_body = ("@staticmethod\n"
                            "def compute_values(values):\n"
                            "  %VALUES%\n"
                            "  a = [1, 2, 3, 4, 5, 6, 7]\n"
                            "  %RETURN%\n")
        self.diagram_widget.add_diagram_item(ni)

    def add_2d_plot_node(self):
        ni = PlotItem2d()
        ni.center = QPoint(randint(1, 400), randint(1, 400))
        self.diagram_widget.add_diagram_item(ni)

    def calculate(self):
        self.diagram_widget.calculate()
        self.diagram_widget.reload_graph()