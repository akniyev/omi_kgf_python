import numpy as np
import sys
from math import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from FunctionApproximator import *
from numpy.linalg import inv


def k(x, y):
    return 1.0 / (fabs(sin(x + y)) + 0.1)


def f(x):
    return cos(x)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph3d_1 = gl.GLViewWidget()
    axises = gl.GLAxisItem(QVector3D(pi, pi, pi))
    graph3d_1.addItem(axises)
    graph3d_2 = gl.GLViewWidget()
    graph2d_1 = pg.PlotWidget()
    graph2d_2 = pg.PlotWidget()
    graph2d_3 = pg.PlotWidget()
    graph2d_4 = pg.PlotWidget()

    # making new approximator
    fa = FunctionApproximator()
    fa.grid_size = 128

    # making discrete functions from above
    k_discrete = np.array(fa.discretize_function_2d(k))
    f_discrete = np.array(fa.discretize_function_1d(f))

    # computing coefficients
    k_coeffs = np.array(fa.calculate_fourier_transform_2d_fast(k_discrete))
    f_coeffs = np.array(fa.calculate_fourier_transform_1d_fast(f_discrete))

    # computing grid to draw this discrete functions
    x_grid = np.array(fa.get_grid())
    y_grid = np.array(fa.get_grid())

    # computing g coefficients
    k = k_coeffs
    f = f_coeffs
    kt = k.transpose()
    ktk_1 = inv(kt.dot(k))
    g_coeffs = ktk_1.dot(kt).dot(f)
    g_restored = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs))

    # drawing functions and coefficients
    k_3d_plot = gl.GLSurfacePlotItem(x=x_grid, y=y_grid, z=k_discrete, color=(1, 0, 0, 1), shader='shaded')
    graph3d_1.addItem(k_3d_plot)

    k_coeff_3d_plot = gl.GLSurfacePlotItem(x=x_grid, y=y_grid, z=k_coeffs, color=(1, 0, 0, 1), shader='shaded')
    graph3d_2.addItem(k_coeff_3d_plot)

    graph2d_1.plotItem.plot(x_grid, f_discrete)
    graph2d_2.plotItem.plot(f_coeffs, symbol='o')

    graph2d_3.plotItem.plot(x_grid, g_coeffs, "Calculated coefficients of g")
    graph2d_4.plotItem.plot(x_grid, g_restored, "Calculated values of g")

    # adding plots to tab bar
    tab_widget = QTabWidget()
    tab_widget.addTab(graph3d_1, "k(x, y)")
    tab_widget.addTab(graph3d_2, "k(x, y) coefficients")

    tab_widget.addTab(graph2d_1, "f(x)")
    tab_widget.addTab(graph2d_2, "f(x) coefficients")
    tab_widget.addTab(graph2d_3, "g(x) coefficients (restored)")
    tab_widget.addTab(graph2d_4, "g(x) values (restored)")

    
    # adding table views
    table_widget = QTableWidget()
    table_widget.setRowCount(k_coeffs.shape[0])
    table_widget.setColumnCount(k_coeffs.shape[1])
    for r in range(k_coeffs.shape[0]):
        for c in range(k_coeffs.shape[1]):
            table_widget.setItem(r, c, QTableWidgetItem("{:15.10f}".format(k_coeffs[r, c])))

    tab_widget.addTab(table_widget, "k(x, y) coefficients table")

    tab_widget.show()
    sys.exit(app.exec_())


