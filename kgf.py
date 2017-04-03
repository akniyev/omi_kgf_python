import numpy as np
import sys
from math import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from FunctionApproximator import *
from numpy.linalg import inv
from SettingsPanel import *


def k(x, y):
    C = 0.1
    return 1.0 / (x ** 2 + y ** 2 + C)
    # return 1.0 / (fabs(sin(x + y)) + 0.1)
    # return 1.0 / (fabs(sin((x + y) / 0.50255)) + 0.1) # from about 1.04 to 1.05 it becomes more and more unstable
    # return 1.0 / (fabs(sin(x) * cos(x) + sin(y)) + 0.1)
    # return 1.0 / (fabs(sin(x + y)) + fabs(cos(x)) + fabs(cos(y)) + 0.1) + fabs(sin(x))
    # return 1.0 / ((x + y) ** 0.5 + sin(x) + 0.1)
    # return 1.0 / (fabs(sin(x) * cos(y)) + 0.1)


def f(x):
    return sin(3*x) / x
    # return fabs(cos(3 * x))
    # return 1 / (sin(x) + 0.1)

params = [
        {'name': 'N', 'type': 'int', 'value': 64},
        {'name': 'M', 'type': 'int', 'value': 16}
    ]

settings_panel = SettingsPanel(params)

def calculate():
    settings_panel.button_calculate.pressed.connect(calculate)

    # making new approximator
    fa = FunctionApproximator()
    fa.grid_size = 256
    M = 16

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
    k = k_coeffs[0:, 0:M - 1]
    f = f_coeffs
    kt = k.transpose()
    ktk_1 = inv(kt.dot(k))
    g_coeffs = ktk_1.dot(kt).dot(f)

    N = fa.grid_size

    # adding zeros
    zeros = np.zeros(N - M + 1)
    g_coeffs = np.append(g_coeffs, zeros)

    g_restored = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs))

    # computing restored f from k(x, y) and obtained g(x)
    f_restored = np.array([0.0 for i in range(x_grid.shape[0])])
    for i in range(x_grid.shape[0]):
        f_i = 0
        for j in range(y_grid.shape[0]):
            f_i += k_discrete[i, j] * g_restored[j]
        f_i = f_i * 2.0 / fa.grid_size  # TODO: I need to find out why this scaling coefficient is needed
        f_restored[i] = f_i


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    hbox = QHBoxLayout()
    window.setLayout(hbox)

    settings_panel.button_calculate.pressed.connect(calculate)

    graph3d_1 = gl.GLViewWidget()
    axises = gl.GLAxisItem(QVector3D(pi, pi, pi))
    graph3d_1.addItem(axises)
    graph3d_2 = gl.GLViewWidget()
    graph2d_1 = pg.PlotWidget()
    graph2d_2 = pg.PlotWidget()
    graph2d_3 = pg.PlotWidget()
    graph2d_4 = pg.PlotWidget()
    graph2d_5 = pg.PlotWidget()

    # making new approximator
    fa = FunctionApproximator()
    fa.grid_size = 256
    M = 16

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
    k = k_coeffs[0:, 0:M-1]
    f = f_coeffs
    kt = k.transpose()
    ktk_1 = inv(kt.dot(k))
    g_coeffs = ktk_1.dot(kt).dot(f)

    N = fa.grid_size

    # adding zeros
    zeros = np.zeros(N - M + 1)
    g_coeffs = np.append(g_coeffs, zeros)

    g_restored = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs))

    # drawing functions and coefficients
    k_3d_plot = gl.GLSurfacePlotItem(x=x_grid, y=y_grid, z=k_discrete, color=(1, 0, 0, 1), shader='shaded')
    graph3d_1.addItem(k_3d_plot)

    k_coeff_3d_plot = gl.GLSurfacePlotItem(x=x_grid, y=y_grid, z=k_coeffs, color=(1, 0, 0, 1), shader='shaded')
    graph3d_2.addItem(k_coeff_3d_plot)

    gp1_1 = graph2d_1.plot()
    gp1_1.setData(x=x_grid, y=f_discrete)

    graph2d_2.plotItem.plot(f_coeffs, symbol='o')

    gp3 = graph2d_3.plot()
    gp4 = graph2d_4.plot()

    gp3.setData(x=x_grid, y=g_coeffs)
    gp4.setData(x=x_grid, y=g_restored)

    # computing restored f from k(x, y) and obtained g(x)
    f_restored = np.array([0.0 for i in range(x_grid.shape[0])])
    for i in range(x_grid.shape[0]):
        f_i = 0
        for j in range(y_grid.shape[0]):
            f_i += k_discrete[i, j] * g_restored[j]
        f_i = f_i * 2.0 / fa.grid_size # TODO: I need to find out why this scaling coefficient is needed
        f_restored[i] = f_i

    # plot restored f(x)
    # pg.plot(x_grid, f_restored, title='f(x) restored')
    # graph2d_1.plotItem.addLine()
    gp5 = graph2d_5.plot()
    gp5.setData(x=x_grid, y=f_restored)

    gp1_2 = graph2d_1.plot()
    gp1_2.setPen((200, 50, 50))
    gp1_2.setData(x=x_grid, y=f_restored)


    # adding plots to tab bar
    tab_widget = QTabWidget()
    tab_widget.addTab(graph3d_1, "k(x, y)")
    tab_widget.addTab(graph3d_2, "k(x, y) coefficients")

    tab_widget.addTab(graph2d_1, "f(x)")
    tab_widget.addTab(graph2d_2, "f(x) coefficients")
    tab_widget.addTab(graph2d_3, "g(x) coefficients (restored)")
    tab_widget.addTab(graph2d_4, "g(x) values (restored)")
    tab_widget.addTab(graph2d_5, "f(x) restored")


    # adding table views
    table_widget = QTableWidget()
    table_widget.setRowCount(k_coeffs.shape[0])
    table_widget.setColumnCount(k_coeffs.shape[1])
    for r in range(k_coeffs.shape[0]):
        for c in range(k_coeffs.shape[1]):
            table_widget.setItem(r, c, QTableWidgetItem("{:15.10f}".format(k_coeffs[r, c])))

    tab_widget.addTab(table_widget, "k(x, y) coefficients table")

    hbox.addWidget(tab_widget)
    settings_panel.setFixedWidth(250)
    hbox.addWidget(settings_panel)

    window.show()
    sys.exit(app.exec_())


