import sys

from math import *
from PyQt5.QtWidgets import QApplication

from MultiPlot2d import MultiPlot2d

m = 8
xs = [0, 0.2, 0.5, 1, 1.6, 1.9, 2, 2.5, pi]
ys = [1, 1, 3, 5, 1, 8, 8, 6, 3]

def alpha(i):
    return (ys[i+1] - ys[i]) / (cos(xs[i+1]) - cos(xs[i]))

def beta(i):
    return ys[i] - cos(xs[i]) * (ys[i+1] - ys[i])/(cos(xs[i+1]) - cos(xs[i]))

def l(x):
    i = 0
    while (not (xs[i] <= x and xs[i+1] >= x)) and (i < len(xs) - 1):
        i += 1
    print(x)
    print(i)
    return alpha(i) * cos(x) + beta(i)

def t(i, N):
    return i * (pi / (N - 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    plot = MultiPlot2d()
    plot.add_plot('function')
    plot.add_plot('polycos')

    N = 1024
    pxs = [t(i, N) for i in range(N)]
    pys = [l(x) for x in pxs]

    plot.set_plot_data('function', xs, ys)
    plot.set_plot_data('polycos', pxs, pys)


    plot.refresh()

    plot.show()

    sys.exit(app.exec_())

