import sys

from math import *
from PyQt5.QtWidgets import *

from MultiPlot2d import MultiPlot2d
from scipy.fftpack import dct, idct

f = lambda x: abs(x) * x # (abs(cos(x))) ** 2 + 0.2 * sin(10 * cos(x))
alphas = []
global_xs = []
# m = 17
# xs = [pi * i / m for i in range(m+1)]
# ys = [f(xs[i]) for i in range(m+1)]
#
# def alpha(i):
#     return (ys[i+1] - ys[i]) / (cos(xs[i+1]) - cos(xs[i]))
#
# def beta(i):
#     return ys[i] - cos(xs[i]) * (ys[i+1] - ys[i])/(cos(xs[i+1]) - cos(xs[i]))
#
# def l(x):
#     i = 0
#     while (not (xs[i] <= x and xs[i+1] >= x)) and (i < len(xs) - 1):
#         i += 1
#     print(x)
#     print(i)
#     return alpha(i) * cos(x) + beta(i)
#
# def t(i, N):
#     return i * (pi / (N - 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # xs = [0, 0.2, 0.5, 1, 1.6, 1.9, 2, 2.5, pi]
    # ys = [1, 1, 3, 5, 1, 8, 8, 6, 3]

    N = 5000
    plot = MultiPlot2d()
    plot.add_plot('polygon')
    plot.add_plot('polycos')
    plot.add_plot('function')
    plot.add_plot('polycos_function_diff')
    plot.add_plot('m_sums')
    plot.add_plot('F_sum')
    plot.add_plot('F_sum_minus_f')

    wnd = QWidget()
    vbox = QVBoxLayout()
    wnd.setLayout(vbox)
    btn = QPushButton("Calculate")
    btn2 = QPushButton("Calculate m-sum")
    btn3 = QPushButton("Calculate F-sum")
    txt = QLineEdit("m&n")
    txt.setText("50")
    txt_k = QLineEdit("k=")
    txt_n = QLineEdit("n=")
    txt_k.setPlaceholderText("k=")
    txt_k.setText("10")
    txt_n.setPlaceholderText("n=")
    txt_n.setText("10")
    vbox.addWidget(txt)
    vbox.addWidget(btn)
    vbox.addWidget(txt_k)
    vbox.addWidget(btn2)
    vbox.addWidget(txt_n)
    vbox.addWidget(btn3)

    wnd.show()


    def calculate():
        m = int(txt.text())
        xs = [pi * i / m for i in range(m + 1)]
        ys = [f(xs[i]) for i in range(m + 1)]

        def alpha(i):
            return (ys[i + 1] - ys[i]) / (cos(xs[i + 1]) - cos(xs[i]))

        def beta(i):
            return ys[i] - cos(xs[i]) * (ys[i + 1] - ys[i]) / (cos(xs[i + 1]) - cos(xs[i]))

        def l(x):
            i = 0
            while (i < len(xs) - 2) and (not (xs[i] <= x and xs[i + 1] >= x)):
                i += 1
            if i >= len(xs):
                i = len(xs) - 1
            return alpha(i) * cos(x) + beta(i)

        def t(i, N):
            return i * (pi / (N - 1))

        pxs = [t(i, N) for i in range(N)]
        pys = [l(x) for x in pxs]

        fys = [f(pxs[i]) for i in range(N)]
        c_fys = [abs(fys[i] - pys[i]) for i in range(N)]

        plot.set_plot_data('polygon', xs, ys)
        plot.set_plot_data('polycos', pxs, pys)
        plot.set_plot_data('function', pxs, fys)
        plot.set_plot_data('polycos_function_diff', pxs, c_fys)

        plot.refresh()


    def calculate_m_sum():
        m = int(txt.text())
        k = int(txt_k.text())

        xs = [pi * i / m for i in range(m + 1)]
        ys = [f(xs[i]) for i in range(m + 1)]

        def alpha(i):
            return (ys[i + 1] - ys[i]) / (cos(xs[i + 1]) - cos(xs[i]))

        def m_sum_for_k(k):
            sum = 0
            for i in range(m):
                sum += alpha(i) * sin(k * (xs[i+1] - xs[i]) / 2) * sin(k * (xs[i+1] - xs[i]) / 2)
            return sum

        # print(m_sum_for_k(k))

        m_sums = [m_sum_for_k(i) for i in range(1000)]
        m_sums_xs = [i for i in range(1000)]

        plot.set_plot_data('m_sums', m_sums_xs, m_sums)
        plot.refresh()

        # print(max(m_sums))


    def calculate_F_sum():
        m = int(txt.text())
        n = int(txt_n.text())

        calculate_F_sum_with_params(m, n)

    def calculate_F_sum_with_params(m, n):
        xs = [pi * i / m for i in range(m + 1)]
        ys = [f(xs[i]) for i in range(m + 1)]

        def alpha(i):
            return (ys[i + 1] - ys[i]) / (cos(xs[i + 1]) - cos(xs[i]))

        def beta(i):
            return ys[i] - cos(xs[i]) * (ys[i + 1] - ys[i]) / (cos(xs[i + 1]) - cos(xs[i]))

        def t(i, N):
            return i * (pi / (N - 1))

        def l(x):
            i = 0
            while (i < len(xs) - 2) and (not (xs[i] <= x and xs[i + 1] >= x)):
                i += 1
            if i >= len(xs):
                i = len(xs) - 1
            return alpha(i) * cos(x) + beta(i)


        N = 300000
        nn = 100000
        l_disc_x = [t(i, N) for i in range(N)]
        l_disc_y = [l(x) for x in l_disc_x]

        l_disc_coeffs = [c / N for c in dct(l_disc_y)]

        for i in range(n+1, N):
            l_disc_coeffs[i] = 0


        l_disc_y_restored = [c / 2 for c in idct(l_disc_coeffs)]

        f_disc_diff = [l_disc_y_restored[i] - f(l_disc_x[i]) for i in range(N)]

        print("n = %.0f, Sn-f = %.20f" % (n, max(f_disc_diff[:nn])))
        # print(max(f_disc_diff))
        # def a0():
        #     sum = 0
        #
        #     for i in range(m):
        #         sum += alpha(i) * (sin(xs[i+1]) - sin(xs[i])) + beta(i) * (xs[i+1] - xs[i])
        #
        #     sum *= 2 / pi
        #
        #     return sum
        #
        # def a1():
        #     sum = 0
        #
        #     for i in range(m):
        #         sum += alpha(i) * (0.5 * (xs[i+1] - xs[i]) - 0.25 * (sin(2*xs[i+1]) - sin(2*xs[i])))
        #
        #     sum *= 2 / pi
        #     return sum
        #
        # def a(k):
        #     sum = 0
        #     for i in range(m):
        #         sum += alpha(i) * ((cos((k-1) * xs[i+1]) - cos((k-1) * xs[i])) / (k - 1) - ((cos((k+1) * xs[i+1]) - cos((k+1) * xs[i])) / (k + 1)))
        #     sum *= 1.0 / (pi * k)
        #
        #     return sum
        #
        # def S(n, x):
        #     sum = a0() / 2 + a1() * cos(x)
        #     for k in range(2, n):
        #         sum += a(k) * cos(k * x)
        #
        #     return sum
        #
        #
        # N1 = 300
        # pxs = [t(i, N1) for i in range(N1)]
        # pys = [S(n, x) for x in pxs]
        #
        # print(pys)

        plot.set_plot_data('F_sum', l_disc_x, l_disc_y_restored)
        plot.set_plot_data('F_sum_minus_f', l_disc_x, f_disc_diff)
        plot.refresh()


    # calculate_F_sum_with_params(1, 1)
    # calculate_F_sum_with_params(2, 2)
    # calculate_F_sum_with_params(4, 4)
    # calculate_F_sum_with_params(8, 8)
    # calculate_F_sum_with_params(10, 10)
    # calculate_F_sum_with_params(16, 16)
    # calculate_F_sum_with_params(20, 20)
    # calculate_F_sum_with_params(40, 40)
    # calculate_F_sum_with_params(80, 80)
    # calculate_F_sum_with_params(100, 100)
    # calculate_F_sum_with_params(200, 200)
    # calculate_F_sum_with_params(400, 400)
    # calculate_F_sum_with_params(800, 800)
    # calculate_F_sum_with_params(1000, 1000)
    # calculate_F_sum_with_params(10000, 10000)

    plot.show()
    btn.pressed.connect(calculate)
    btn2.pressed.connect(calculate_m_sum)
    btn3.pressed.connect(calculate_F_sum)

    sys.exit(app.exec_())

