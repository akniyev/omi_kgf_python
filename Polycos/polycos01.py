import sys

from math import *
from PyQt5.QtWidgets import *
from numpy import array_equal

from MultiPlot2d import MultiPlot2d
from Polycos.FunctionApproximation import *

f = lambda x: abs(cos(x / 2)) ** 3
max_msum = 0.0

def calculate_l(f: Callable[[float], float], node_xs: List[float], out_discretization: int) -> Tuple[List[float], List[float]]:
    m = len(node_xs) - 1
    N = out_discretization
    xs = [pi * i / (N-1) for i in range(N)]
    node_ys = [f(node_xs[i]) for i in range(m + 1)]

    def alpha(i):
        return (node_ys[i + 1] - node_ys[i]) / (cos(node_xs[i + 1]) - cos(node_xs[i]))

    def beta(i):
        return node_ys[i] - cos(node_xs[i]) * (node_ys[i + 1] - node_ys[i]) / (cos(node_xs[i + 1]) - cos(node_xs[i]))

    def l(x):
        i = 0
        while (i < len(node_xs) - 2) and (not (node_xs[i] <= x and node_xs[i + 1] >= x)):
            i += 1
        if i >= len(node_xs):
            i = len(node_xs) - 1
        return alpha(i) * cos(x) + beta(i)

    ys = [l(x) for x in xs]

    return (xs, ys)

def calculate_Rn(f: Callable[[float], float], node_xs: List[float], n: int, max_k: int, out_discretization: int) -> Tuple[List[float], List[float]]:
    m = len(node_xs) - 1
    N = out_discretization
    xs = [pi * i / (N-1) for i in range(N)]
    node_ys = [f(node_xs[i]) for i in range(m + 1)]

    def alpha(i):
        return (node_ys[i + 1] - node_ys[i]) / (cos(node_xs[i + 1]) - cos(node_xs[i]))

    def R(x):
        result = 0.0
        for k in range(n, max_k):
            msum = 0.0
            for i in range(1, m):
                msum += (alpha(i-1) - alpha(i)) * ((sin((k-1)*node_xs[i]))/(k-1) - (sin((k+1)*node_xs[i]))/(k+1))
                # msum += (alpha(i - 1) - alpha(i)) * ((sin((k - 1) * node_xs[i])))
            result += (cos(k*x) / k) * msum
            global max_msum
            if abs(msum) > max_msum:
                max_msum = abs(msum)
        result *= 1/pi
        return result

    def R2(x):
        result = 0.0
        for i in range(1, m):
            ksum = 0.0
            for k in range(n+1, max_k):
                jsum = 0.0
                for j in range(1, k+1):
                    jsum += cos(j*x) * sin((j-1) * x)
                ksum += 2 / (k * (k * k - 1)) * jsum
            result += (alpha(i-1) - alpha(i)) * ksum
        return result

    global max_msum
    max_msum = 0.0
    ys = [abs(R(x)) for x in xs]
    print("max_m_sum = %s" % max_msum)
    return (xs, ys)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    plot = MultiPlot2d()

    plot.add_plot('function', (0, 0, 0), 'Original function f')
    plot.add_plot('Sn', (255, 0, 0), 'Partial fourier sum of order n', False)
    plot.add_plot('f-Sn', (128, 128, 128), 'Difference between the function and its Fourier sum', False)
    plot.add_plot('l(f)', (0, 255, 0), 'Polycos inscribed in the function f', False)
    plot.add_plot('f-l(f)', (128, 128, 0), 'Difference between the function f and l(f)', False)
    plot.add_plot('Sn(l(f))', (128, 128, 0), 'Fourier sum for the function l(f)', False)
    plot.add_plot('l(f)-Sn(l(f))', (128, 0, 128), 'Difference between the function l(f) and its Fourier sum', False)
    plot.add_plot('f-Sn(l(f))', (128, 0, 128), 'Difference between the function f and Fourier sum for l(f)', False)
    plot.add_plot('Rn', (0, 255, 128), 'Calculated Rn(l,x)', False)

    # Create a window with controls

    wnd = QWidget()
    vbox = QVBoxLayout()
    wnd.setLayout(vbox)

    txt_n = QLineEdit("n=")
    txt_n.setText("10")
    lbl_n = QLabel("n = ")

    txt_m = QLineEdit("m=")
    txt_m.setText("10")
    lbl_m = QLabel("m = ")

    txt_N = QLineEdit("N=")
    txt_N.setText("100000")
    lbl_N = QLabel("N (x-axis discretization)")

    btn_calculate = QPushButton("Calculate")

    vbox.addWidget(lbl_n)
    vbox.addWidget(txt_n)

    vbox.addWidget(lbl_m)
    vbox.addWidget(txt_m)

    vbox.addWidget(lbl_N)
    vbox.addWidget(txt_N)

    vbox.addWidget(btn_calculate)

    wnd.setGeometry(10, 10, 300, 100)
    wnd.show()


    def calculate():
        N = int(txt_N.text())
        # Attention: all the xs should have the same size

        # Drawing the function f
        f_xs = [pi * i / (N - 1) for i in range(N)]
        f_ys = [f(x) for x in f_xs]

        plot.set_plot_data('function', f_xs, f_ys)

        # Drawing the partial Fourier sums
        n = int(txt_n.text())

        fcoeffs = fourierCoefficientsForEvenFunction(f, n, N)
        (fourier_xs, fourier_ys) = functionFromCoefficientsForEvenFunction(fcoeffs, N)

        plot.set_plot_data('Sn', fourier_xs, fourier_ys)

        # Drawing the difference between the function f and its Fourier sum
        diff_ys = [abs(f_y - fourier_y) for f_y, fourier_y in zip(f_ys, fourier_ys)]
        plot.set_plot_data('f-Sn', f_xs, diff_ys)

        # Drawing l(x)
        m = int(txt_m.text())
        node_xs = [pi * i / m for i in range(m + 1)]
        (l_xs, l_ys) = calculate_l(f, node_xs, N)
        plot.set_plot_data('l(f)', l_xs, l_ys)

        # Drawing the difference between the function f and l(f)
        diff_f_l = [abs(f - l) for f, l in zip(f_ys, l_ys)]
        plot.set_plot_data('f-l(f)', l_xs, diff_f_l)

        # Drawing Fourier sums for the function f
        l_coeffs = fourierCoefficientsForEvenFunctionPreCalculated(l_ys, n, N)
        (fourier_l_xs, fourier_l_ys) = functionFromCoefficientsForEvenFunction(l_coeffs, N)
        plot.set_plot_data('Sn(l(f))', fourier_l_xs, fourier_l_ys)

        # Difference between the function l(f) and Sn(l(f))
        l_Sn_l_diff_ys = [abs(l - Snl) for l, Snl in zip(l_ys, fourier_l_ys)]
        plot.set_plot_data('l(f)-Sn(l(f))', l_xs, l_Sn_l_diff_ys)

        # Difference between the function f and Sn(l(f))
        f_Sn_l_diff_ys = [abs(fx - Snl) for fx, Snl in zip(f_ys, fourier_l_ys)]
        plot.set_plot_data('f-Sn(l(f))', l_xs, f_Sn_l_diff_ys)

        # Rn(l,x)
        N_Rn = 100
        max_k = 100
        (Rn_xs, Rn_ys) = calculate_Rn(f, node_xs, n + 1, max_k, N_Rn)
        plot.set_plot_data('Rn', Rn_xs, Rn_ys)

        # After all the calculations
        plot.refresh()

    plot.show()
    btn_calculate.pressed.connect(calculate)

    sys.exit(app.exec_())

