import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from numpy.ma import arccos, cos

from MultiPlot2d import MultiPlot2d


def theta(i, N):
    return arccos(-1 + 2 * i / (N - 1))


def diff(j, x, N):
    theta_j = theta(j, N)
    theta_j_1 = theta(j+1, N)
    a1 = (cos(x) - cos(theta_j)) / (cos(theta_j_1 - theta_j))
    a2 = (x - theta_j) / (theta_j_1 - theta_j)
    return a1 - a2


if __name__ == '__main__':
    app = QApplication(sys.argv)

    plot = MultiPlot2d()

    N = 20
    n = 15

    x = [0 for i in range(n+1)]
    y = [0 for i in range(n+1)]
    j = 1

    print(x)
    print(y)

    a = theta(j, N)
    b = theta(j + 1, N)

    for i in range(n+1):
        x[i] = a + 2*((b - a) / n) * i
        y[i] = diff(j, x[i], N)

    print(a)
    print(b)
    print('x = ')
    for item in x:
        print(item)

    print('y = ')

    for item in y:
        print(item)

    plot.show()

    sys.exit(app.exec_())
