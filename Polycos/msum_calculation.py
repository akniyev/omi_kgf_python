import sys

from math import *
from PyQt5.QtWidgets import *
from numpy import array_equal

from MultiPlot2d import MultiPlot2d
from Polycos.FunctionApproximation import *

f = lambda x: abs(cos(x)) ** 3
max_msum = 0.0

def calculate_Rn(f: Callable[[float], float], node_xs: List[float], n: int, max_k: int, out_discretization: int) -> Tuple[List[float], List[float]]:
    m = len(node_xs) - 1
    print("m = %i" % m)
    N = out_discretization
    node_ys = [f(node_xs[i]) for i in range(m + 1)]

    def alpha(i):
        return (node_ys[i + 1] - node_ys[i]) / (cos(node_xs[i + 1]) - cos(node_xs[i]))

    # def R(x):
    #     result = 0.0
    #     for k in range(n, max_k):
    #         msum = 0.0
    #         for i in range(1, m):
    #             msum += (alpha(i-1) - alpha(i)) * ((sin((k-1)*node_xs[i]))/(k-1) - (sin((k+1)*node_xs[i]))/(k+1))
    #         result += cos(k*x) / k * msum
    #         global max_msum
    #         if abs(msum) > max_msum:
    #             max_msum = abs(msum)
    #     result *= 1/pi
    #     return result

    def msum(k):
        s = 0.0
        for i in range(1, m):
            s += ((sin((k)*node_xs[i])))
        return s

    xs = [k for k in range(m+1, max_k)]
    ys = [msum(k)/k for k in xs]

    # xs = [i for i in range(1, m-1)]
    # ys = [2 * alpha(i) - alpha(i + 1) - alpha(i - 1) for i in range(1, m-1)]

    return (xs, ys)

def calculate_msum_part(node_xs: List[float], k: int, i: int, out_discretization: int) -> Tuple[List[float], List[float]]:
    m = len(node_xs) - 1
    N = out_discretization
    node_ys = [f(node_xs[i]) for i in range(m + 1)]

    def alpha(i):
        return (node_ys[i + 1] - node_ys[i]) / (cos(node_xs[i + 1]) - cos(node_xs[i]))

    def msum_2(k, i, x):
        s = 0.0
        for j in range(1, k+1):
            s += cos(j * x) * sin((j - 1) * node_xs[i])


    xs = node_xs
    ys = [msum_2(k, i, x) for x in xs]

    # xs = [i for i in range(1, m-1)]
    # ys = [2 * alpha(i) - alpha(i + 1) - alpha(i - 1) for i in range(1, m-1)]

    return (xs, ys)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    plot = MultiPlot2d()

    plot.add_plot('Rn', (128, 255, 128), 'msum', True)
    plot.add_plot('sin', (128, 255, 0), 'sin', True)

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
    txt_N.setText("300")
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
        # Rn(l,x)
        N = int(txt_N.text())
        m = int(txt_m.text())
        n = int(txt_n.text())
        node_xs = [pi * i / m for i in range(m + 1)]
        max_k = 10000
        (Rn_xs, Rn_ys) = calculate_Rn(f, node_xs, n + 1, max_k, N)
        plot.set_plot_data('Rn', Rn_xs, Rn_ys)

        sin_ys = [(1 - (-1) ** k) / (2 * abs(sin(pi * k / (2 * m)))) for k in Rn_xs]
        plot.set_plot_data('sin', Rn_xs, sin_ys)

        # After all the calculations
        plot.refresh()

    plot.show()
    btn_calculate.pressed.connect(calculate)

    sys.exit(app.exec_())

