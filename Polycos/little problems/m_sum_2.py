from math import sin, cos, pi
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication


def print_m_sum(m, k):
    x = lambda i: pi * i / m
    f = lambda x: abs(cos(x/2)) ** 3

    def alpha(i):
        return (f(x(i+1)) - f(x(i))) / (cos(x(i+1)) - cos(x(i)))

    s = sum([(alpha(i-1) - alpha(i)) * sin((k-1) * x(i)) for i in range(1, m)])
    return s

def alpha_diff(m):
    xi = lambda i: pi * i / m
    f = lambda x: abs(sin(x)) ** 3

    def alpha(i):
        return (f(xi(i+1)) - f(xi(i))) / (cos(xi(i+1)) - cos(xi(i)))

    result = [((alpha(i-1) - alpha(i)) - (alpha(i) - alpha(i+1)))  for i in range(1, m-1)]

    for j in range(m-2):
        if abs(result[j]) > 1000:
            result[j] = 0

    return result

m = 10000

app = QApplication([])

xs = [i for i in range(1, m - 1)]
ys = alpha_diff(m)

pg.plot(xs, ys)

app.exec_()

# for k in range(m + 1, 10000):
#     s = print_m_sum(m, k)
#     print("%2.5f" % abs(s))

# def mysum(m, x):
#     x_ = lambda i: pi * i / m
#     lsum = 0.0
#     for l in range(1, m):
#         jsum = 0.0
#         for j in range(1, l+1):
#             jsum += cos(j * x) * sin((j-1) * x_(l))
#         lsum += jsum
#     return lsum
#
# prev_r = 1.0
# for i in range(2, 20):
#     m = 2 ** i
#     r = max([mysum(m, pi * j / m) for j in range(0, m+1)])
#     print("m = %10i, sum = %3.10f, growth: %3.4f" % (m, r, r / prev_r))
#     prev_r = r

# app = QApplication([])
#
# sum_k = [print_m_sum(m, k) for k in range(m + 1, 10000)]
# sum_k_xs = [i for i in range(m + 1, 10000)]
#
# pg.plot(sum_k_xs, sum_k)
#
# app.exec_()


