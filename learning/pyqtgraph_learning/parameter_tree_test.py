import sys
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from pyqtgraph.parametertree import *



if __name__ == '__main__':
    params = [
        {'name': 'N', 'type': 'int', 'value': 64},
        {'name': 'M', 'type': 'int', 'value': 16}
    ]

    app = QApplication(sys.argv)

    settings_panel = QWidget()
    vbox = QVBoxLayout()
    button_calculate = QPushButton('Calculate')

    t = ParameterTree()

    param_group = Parameter.create(name='Parameters', type='group', children=params)

    t.setParameters(param=param_group)

    vbox.addWidget(t)
    vbox.addWidget(button_calculate)
    settings_panel.setLayout(vbox)

    settings_panel.show()
    sys.exit(app.exec_())

