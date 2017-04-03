from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from pyqtgraph.parametertree import *


class SettingsPanel(QWidget):
    def __init__(self, params):
        super().__init__()
        vbox = QVBoxLayout()
        t = ParameterTree()

        self.button_calculate = QPushButton('Calculate')
        self.parameter = Parameter.create(name='Parameters', type='group', children=params)

        t.setParameters(param=self.parameter)

        vbox.addWidget(t)
        vbox.addWidget(self.button_calculate)
        self.setLayout(vbox)


