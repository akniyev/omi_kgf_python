from math import sin, cos, pi
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication


def x_(i, m):
    return pi * i / m

# for m in range(3, 50):
#     print("*********** m = %i ************" % m)
#     for i in range(1,m-1):
#         print("m = %i, i = %i, sinx_i/sinx_{i+1} = %f)" % (m, i, 1-  sin(x(i, m)) / sin(x(i+1, m))))
#         # print("m = %i, i = %i, sinx_i/sinx_{i+1} = %f)" % (m, i, (cos(x(i+1, m)) - cos(x(i-1, m))) / (cos(x(i+2, m)) - cos(x(i,m)))))

# sum = 0.0
# m = 10
# n = m
# x = pi / 2
# i = 5
#
# for k in range(n + 1, 10000):
#     sum += (cos(k * x) * sin((k-1) * x_(i, m))) / (k * (k - 1))
#
# print(abs(sum))

def est_sum(x, k, i, m):
    xi = lambda i: pi * i / m
    sum = 0.0
    for j in range(1, k + 1):
        lsum = 0.0
        for l in range(1, i + 1):
            lsum += sin((j-1) * xi(l))
        sum += cos(j * x) * lsum
    return sum

# app = QApplication([])
#
# N = 5000
# k = 500
# i = 10
# m = 20
# xs = [i * pi / N for i in range(N + 1)]
# ys = [abs(est_sum(x, k, i, m)) for x in xs]
#
# pg.plot(xs, ys)
#
# app.exec_()


def sum2(i, j, m, x):
    result = 0.0
    for l in range(1, i + 1):
        result += cos(j*x) * sin((j - 1) * pi * l / m)
    return result

m = 100
j = 250
x = 0
N = 100

for o in range(1, N + 1):
    max_sum = max([abs(sum2(i, j, m, x)) for i in range(1, m)])
    x = o * pi / N
    print("x = %3.2f, max_sum = %2.10f" % (x, max_sum))