import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from math import *


def k(x, y):
    return cos(x) * cos(y)


def node(i, n):
    return (2.0 * i + 1.0) * pi / (2.0 * n)


def grid_nodes(n):
    return np.array([node(i, n) for i in range(n)])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()

    vbox = QVBoxLayout()

    # adding grid
    view = gl.GLViewWidget()

    # g = gl.GLGridItem()
    # g.scale(2, 2, 1)
    # g.setDepthValue(10)
    # g.setSize(x=2 * pi, y=2*pi)
    # view.addItem(g)

    # calculating function and drawing it on the view
    n = 256

    xs = grid_nodes(n)
    ys = grid_nodes(n)

    zs = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            x = xs[i]
            y = ys[j]
            zs[i][j] = k(x, y)
    zs = np.array(zs)

    zs1 = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            x = xs[i]
            y = ys[j]
            zs1[i][j] = k(x, y) * 0.9
    zs1 = np.array(zs1)

    function_plot = gl.GLSurfacePlotItem(x=xs, y=ys, z=zs, color=(1, 0, 0, 1), shader='shaded')
    view.addItem(function_plot)
    function_plot = gl.GLSurfacePlotItem(x=xs, y=ys, z=zs1, color=(0, 1, 0, 1), shader='shaded')
    view.addItem(function_plot)

    # add axises
    axises = gl.GLAxisItem(QtGui.QVector3D(pi, pi, pi))
    view.addItem(axises)

    vbox.addWidget(view)

    hbox = QHBoxLayout()

    btn1 = QPushButton()
    btn2 = QPushButton()
    btn3 = QPushButton()

    hbox.addWidget(btn1)
    hbox.addWidget(btn2)
    hbox.addWidget(btn3)

    vbox.addLayout(hbox)

    widget.setLayout(vbox)

    widget.setGeometry(200, 200, 500, 600)

    widget.show()
    sys.exit(app.exec_())
