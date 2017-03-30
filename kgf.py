import numpy as np
import sys
from math import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl


from FunctionApproximator import *


def k(x, y):
    return cos(x) * cos(y)


def f(x):
    return 1.0 / (fabs(x) + 0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph3d_1 = gl.GLViewWidget()
    axises = gl.GLAxisItem(QVector3D(pi, pi, pi))
    graph3d_1.addItem(axises)
    graph3d_2 = gl.GLViewWidget()
    graph2d_1 = pg.PlotWidget()
    graph2d_2 = pg.PlotWidget()

    # making new approximator
    fa = FunctionApproximator()
    fa.grid_size = 128

    # making discrete functions from above
    k_discrete = np.array(fa.discretize_function_2d(k))
    f_discrete = np.array(fa.discretize_function_1d(f))

    k_coeffs = np.array(fa.calculate_fourier_transform_2d_fast(k_discrete))
    f_coeffs = np.array(fa.calculate_fourier_transform_1d_fast(f_discrete))

    x_grid = np.array(fa.get_grid())
    y_grid = np.array(fa.get_grid())

    k_3d_plot = gl.GLSurfacePlotItem(x=x_grid, y=y_grid, z=k_discrete, color=(1, 0, 0, 1), shader='shaded')
    graph3d_1.addItem(k_3d_plot)

    k_coeff_3d_plot = gl.GLSurfacePlotItem(x=x_grid, y=y_grid, z=k_coeffs, color=(1, 0, 0, 1), shader='shaded')
    graph3d_2.addItem(k_coeff_3d_plot)

    graph2d_1.plotItem.plot(x_grid, f_discrete)
    graph2d_2.plotItem.plot(f_coeffs, symbol='o')

    tab_widget = QTabWidget()
    tab_widget.addTab(graph3d_1, "k(x, y)")
    tab_widget.addTab(graph3d_2, "k(x, y) coefficients")

    tab_widget.addTab(graph2d_1, "f(x)")
    tab_widget.addTab(graph2d_2, "f(x) coefficients")

    tab_widget.show()
    sys.exit(app.exec_())


