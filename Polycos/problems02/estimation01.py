from typing import Callable, List
from math import sin, cos, pi

import sys

from PyQt5.QtWidgets import QApplication

from MultiPlot2d import MultiPlot2d

def R1_prepare(f: Callable[[float], float], m: int, n: int, INF: int) -> List[float]:
    xi = [pi * i / m for i in range(m+1)]
    sinxi = [sin(x) for x in xi]
    alpha = [(f(xi[i+1]) - f(xi[i])) / (cos(xi[i+1]) - cos(xi[i])) for i in range(m)]

    addends = [0] * INF

    for k in range(n + 1, INF):
        m_sum = 0.0
        for i in range(1,m):
            m_sum += (alpha[i-1] - alpha[i]) * sin((k - 1) * xi[i])

        addends[k] = 2 / (pi * k * (k * k - 1)) * m_sum

    return addends

def R2_prepare(f: Callable[[float], float], m: int, n: int, INF: int) -> List[float]:
    xi = [pi * i / m for i in range(m + 1)]
    sinxi = [sin(x) for x in xi]
    alpha = [(f(xi[i + 1]) - f(xi[i])) / (cos(xi[i + 1]) - cos(xi[i])) for i in range(m)]

    addends = [0] * INF

    for k in range(n + 1, INF):
        (d, m) = divmod(k, 1000)
        if m == 0:
            print("Preparing R2 (%i/%i)" % (k, INF))
        m_sum = 0.0
        for i in range(1,m):
            m_sum += (alpha[i-1] - alpha[i]) * sinxi[i] * cos(k * xi[i])
        addends[k] = 1 / (pi * k * (k + 1)) * m_sum
    return addends

def R(addends, n: int, x: float, INF: int):
    result = 0.0
    for k in range(n + 1, INF):
        result += cos(k * x) * addends[k]

    return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = lambda x: abs(sin(x)) ** 3
    plot = MultiPlot2d()

    plot.add_plot('R1', (128, 255, 128), 'R1')
    plot.add_plot('R2', (255, 128, 128), 'R2')
    plot.add_plot('R', (0, 0, 0), 'R')
    #plot.add_plot('f-Sn', (128, 128, 128), 'Difference between the function and its Fourier sum', False)

    INF = 200000
    N = 40000
    m = 10000
    n = 10000

    # R1_adds = R1_prepare(f, m, n, INF)
    R2_adds = R2_prepare(f, m, n, INF)

    xs = [pi * i / N for i in range(N+1)]
    # R1s = [R(R1_adds, n, x, INF) for x in xs]
    print("Starting...")
    R2s = [R(R2_adds, n, x, INF) for x in xs]
    print("MAX R2: %20.15f" % R(R2_adds, n, pi / 2, INF))
    # plot.set_plot_data('R1', xs, R1s)
    plot.set_plot_data('R2', xs, R2s)
    # plot.set_plot_data('R', xs, [abs(x1 - x2) for (x1, x2) in zip(R1s, R2s)])

    print("MAX R2: %20.15f" % max([abs(x) for x in R2s]))

    plot.refresh()

    plot.show()
    sys.exit(app.exec_())