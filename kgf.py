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
from MultiPlot2d import *
from MultiPlot3d import *


class Form(QWidget):
    def __init__(self):
        super().__init__()
        # Building UI
        params = [
            {'name': 'logN', 'type': 'int', 'value': 5},
            {'name': 'N = ', 'type': 'int', 'readonly': True, 'value': 32},
            {'name': 'M', 'type': 'int', 'value': 16},
            {'name': 'M_rect_hor', 'type': 'int', 'value': 16},
            {'name': 'M_rect_vert', 'type': 'int', 'value': 16},
            {'name': 'M_triangle', 'type': 'int', 'value': 16},
            {'name': 'M_corner', 'type': 'int', 'value': 16},
        ]

        self.settings_panel = SettingsPanel(params)
        self.tab_widget = QTabWidget()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        self.settings_panel.button_calculate.pressed.connect(self.calculate)
        self.settings_panel.setFixedWidth(250)
        hbox.addWidget(self.tab_widget)
        hbox.addWidget(self.settings_panel)
        self.show()

        self.plot_3d_kernel = MultiPlot3d('kernel')
        self.plot_3d_kernel_coeffs = MultiPlot3d('kernel_coeffs')
        self.plot_2d_func_f = MultiPlot2d('f', 'f_restored', 'f_restored_2_square', 'f_restored_3_triangle', 'f_restored_4_corner')
        self.plot2d_coeffs_f = MultiPlot2d('f_coeffs')
        self.plot2d_coeffs_g = MultiPlot2d('g_coeffs', 'g_coeffs_2_square')
        self. plot2d_func_g = MultiPlot2d('g_restored', 'g_restored_2_square')

        self.tab_widget.addTab(self.plot_3d_kernel, 'kernel')
        self.tab_widget.addTab(self.plot_3d_kernel_coeffs, 'kernel coeffs')
        self.tab_widget.addTab(self.plot_2d_func_f, 'f')
        self.tab_widget.addTab(self.plot2d_coeffs_f, 'f coeffs')
        self.tab_widget.addTab(self.plot2d_coeffs_g, 'g coeffs')
        self.tab_widget.addTab(self.plot2d_func_g, 'g restored')
        # end building UI

    @staticmethod
    def print_2d_array_to_file(array_to_print, filename):
        with open(filename, 'w') as file:
            for row in array_to_print:
                for item in row:
                    #file.write("\t\t{}".format(item))
                    file.write('{:5.3f} '.format(item))
                file.write("\n")

    @staticmethod
    def k(x, y):
        C = 0.1
        # return 1.0 / (x ** 2 + y ** 2 + C)
        return 1.0 / (fabs(sin(x + y)) + 0.1)
        # return 1.0 / (fabs(sin((x + y) / 0.50255)) + 0.1) # from about 1.04 to 1.05 it becomes more and more unstable
        # return 1.0 / (fabs(sin(x) * cos(x) + sin(y)) + 0.1)
        # return 1.0 / (fabs(sin(x + y)) + fabs(cos(x)) + fabs(cos(y)) + 0.1) + fabs(sin(x))
        # return 1.0 / ((x + y) ** 0.5 + sin(x) + 0.1)
        # return 1.0 / (fabs(sin(x) * cos(y)) + 0.1)

    @staticmethod
    def f(x):
        return sin(3 * x) / x
        # return fabs(cos(3 * x))
        # return 1 / (sin(x) + 0.1)

    def compute_g_coefficients_1(self, kc, fc, N, M):
        # computing g coefficients
        kc = kc.copy()
        k = kc[0:, 0:M]

        self.print_2d_array_to_file(k, 'k_1_square.del')

        kt = k.transpose()
        ktk_1 = inv(kt.dot(k))
        g_coeffs = ktk_1.dot(kt).dot(fc)

        # adding zeros
        if N - M > 0:
            zeros = np.zeros(N - M)
            g_coeffs = np.append(g_coeffs, zeros)
        return g_coeffs

    def compute_g_coefficients_2(self, kc, fc, N, M_hor, M_vert):
        # computing g coefficients
        kc = kc.copy()
        k = kc[0:, 0:M_hor]
        for row in range(M_vert, N):
            for col in range(M_hor):
                k[row, col] = 0

        self.print_2d_array_to_file(k, 'k_2_rect.del')

        kt = k.transpose()
        ktk_1 = inv(kt.dot(k))
        g_coeffs = ktk_1.dot(kt).dot(fc)

        # adding zeros
        if N - len(g_coeffs) > 0:
            zeros = np.zeros(N - len(g_coeffs))
            g_coeffs = np.append(g_coeffs, zeros)
        return g_coeffs

    def compute_g_coefficients_3_triangle(self, kc, fc, N, M):
        # computing g coefficients
        kc = kc.copy()
        k = kc[0:, 0:M]
        for row in range(M, N):
            for col in range(M):
                k[row, col] = 0
        for row in range(1, M):
            for col in range(M-row, M):
                k[row, col] = 0

        self.print_2d_array_to_file(k, 'k_3_triangle.del')

        kt = k.transpose()
        ktk_1 = inv(kt.dot(k))
        g_coeffs = ktk_1.dot(kt).dot(fc)

        # adding zeros
        if N - M > 0:
            zeros = np.zeros(N - M)
            g_coeffs = np.append(g_coeffs, zeros)
        return g_coeffs

    def compute_g_coefficients_4_corner(self, kc, fc, N, M):
        # computing g coefficients
        kc = kc.copy()
        k = kc[0:, 0:M]
        m = divmod(M, 2)[0]
        for row in range(M, N):
            for col in range(M):
                k[row, col] = 0
        for row in range(m, M):
            for col in range(m, M):
                k[row, col] = 0

        self.print_2d_array_to_file(k, 'k_4_corner.del')

        kt = k.transpose()
        ktk_1 = inv(kt.dot(k))
        g_coeffs = ktk_1.dot(kt).dot(fc)

        # adding zeros
        if N - M > 0:
            zeros = np.zeros(N - M)
            g_coeffs = np.append(g_coeffs, zeros)
        return g_coeffs

    def calculate(self):
        logN = self.settings_panel.parameter['logN']
        M = self.settings_panel.parameter['M']
        M_rect_hor = self.settings_panel.parameter['M_rect_hor']
        M_rect_ver = self.settings_panel.parameter['M_rect_vert']
        M_triangle = self.settings_panel.parameter['M_triangle']
        M_corner = self.settings_panel.parameter['M_corner']

        N = 2 ** logN
        self.settings_panel.parameter['N = '] = N

        if M > N:
            return

        print("N = {}, M = {}".format(N, M))

        # making new approximator
        fa = FunctionApproximator()
        fa.grid_size = N

        # making discrete functions from above
        k_discrete = np.array(fa.discretize_function_2d(self.k))
        f_discrete = np.array(fa.discretize_function_1d(self.f))

        # computing coefficients
        k_coeffs = np.array(fa.calculate_fourier_transform_2d_fast(k_discrete))
        f_coeffs = np.array(fa.calculate_fourier_transform_1d_fast(f_discrete))

        # computing grid to draw this discrete functions
        x_grid = np.array(fa.get_grid())
        y_grid = np.array(fa.get_grid())

        # computing g coefficients
        g_coeffs = self.compute_g_coefficients_1(k_coeffs, f_coeffs, N, M)
        g_coeffs_2_square = self.compute_g_coefficients_2(k_coeffs, f_coeffs, N, M_rect_hor, M_rect_ver)
        g_coeffs_3_triangle = self.compute_g_coefficients_3_triangle(k_coeffs, f_coeffs, N, M_triangle)
        g_coeffs_4_corner = self.compute_g_coefficients_4_corner(k_coeffs, f_coeffs, N, M_corner)

        g_restored = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs))
        g_restored_2_square = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs_2_square))
        g_restored_3_triangle = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs_3_triangle))
        g_restored_4_corner = np.array(fa.calculate_inverse_fourier_transform_1d_fast(g_coeffs_4_corner))


        # computing restored f from k(x, y) and obtained g(x)
        f_restored = np.array([0.0 for i in range(x_grid.shape[0])])
        for i in range(x_grid.shape[0]):
            f_i = 0
            for j in range(y_grid.shape[0]):
                f_i += k_discrete[i, j] * g_restored[j]
            f_i = f_i * 2.0 / fa.grid_size  # TODO: I need to find out why this scaling coefficient is needed
            f_restored[i] = f_i

        f_restored_2_square = np.array([0.0 for i in range(x_grid.shape[0])])
        for i in range(x_grid.shape[0]):
            f_i = 0
            for j in range(y_grid.shape[0]):
                f_i += k_discrete[i, j] * g_restored_2_square[j]
            f_i = f_i * 2.0 / fa.grid_size  # TODO: I need to find out why this scaling coefficient is needed
            f_restored_2_square[i] = f_i

        f_restored_3_triangle = np.array([0.0 for i in range(x_grid.shape[0])])
        for i in range(x_grid.shape[0]):
            f_i = 0
            for j in range(y_grid.shape[0]):
                f_i += k_discrete[i, j] * g_restored_3_triangle[j]
            f_i = f_i * 2.0 / fa.grid_size  # TODO: I need to find out why this scaling coefficient is needed
            f_restored_3_triangle[i] = f_i

        f_restored_4_corner = np.array([0.0 for i in range(x_grid.shape[0])])
        for i in range(x_grid.shape[0]):
            f_i = 0
            for j in range(y_grid.shape[0]):
                f_i += k_discrete[i, j] * g_restored_4_corner[j]
            f_i = f_i * 2.0 / fa.grid_size  # TODO: I need to find out why this scaling coefficient is needed
            f_restored_4_corner[i] = f_i

        # k_discrete
        # k_coeffs
        # f_discrete
        # f_coeffs
        # f_restored
        # g_coeffs
        # g_restored
        # x_grid
        # y_grid

        # self.plot_3d_kernel = MultiPlot3d('kernel')
        # self.plot_3d_kernel_coeffs = MultiPlot3d('kernel_coeffs')
        # self.plot_2d_func_f = MultiPlot2d('f', 'f_restored')
        # self.plot2d_coeffs_f = MultiPlot2d('f_coeffs')
        # self.plot2d_coeffs_g = MultiPlot2d('g_coeffs')
        # self.plot2d_func_g = MultiPlot2d('g_restored')

        self.plot_3d_kernel.set_plot_data('kernel', xs=x_grid, ys=y_grid, zs=k_discrete)
        self.plot_3d_kernel_coeffs.set_plot_data('kernel_coeffs', xs=x_grid, ys=y_grid, zs=k_coeffs)
        self.plot_2d_func_f.set_plot_data('f', xs=x_grid, ys=f_discrete)
        self.plot_2d_func_f.set_plot_data('f_restored', xs=x_grid, ys=f_restored)
        self.plot_2d_func_f.set_plot_data('f_restored_2_square', xs=x_grid, ys=f_restored_2_square)
        self.plot_2d_func_f.set_plot_data('f_restored_3_triangle', xs=x_grid, ys=f_restored_3_triangle)
        self.plot_2d_func_f.set_plot_data('f_restored_4_corner', xs=x_grid, ys=f_restored_4_corner)
        self.plot2d_coeffs_f.set_plot_data('f_coeffs', xs=np.array([i for i in range(len(f_coeffs))]), ys=f_coeffs)
        self.plot2d_coeffs_g.set_plot_data('g_coeffs', xs=np.array([i for i in range(len(g_coeffs))]), ys=g_coeffs)
        self.plot2d_coeffs_g.set_plot_data('g_coeffs_2_square', xs=np.array([i for i in range(len(g_coeffs))]), ys=g_coeffs_2_square)
        self.plot2d_func_g.set_plot_data('g_restored', xs=x_grid, ys=g_restored)
        self.plot2d_func_g.set_plot_data('g_restored_2_square', xs=x_grid, ys=g_restored_2_square)

        self.plot_3d_kernel.refresh()
        self.plot_3d_kernel_coeffs.refresh()
        self.plot_2d_func_f.refresh()
        self.plot2d_coeffs_f.refresh()
        self.plot2d_coeffs_g.refresh()
        self.plot2d_func_g.refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = Form()

    form.show()

    sys.exit(app.exec_())
