from math import sin, cos, pi
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication

# It calculates the sum
# \sum_{i=1}^{m-1}\left(\alpha_{i-1}-\alpha_{i}\right)\sin x_{i}\cos kx_{i} \cos kx / k
def msum(k, m, x = 0):
    xi = lambda i: pi * i / m
    f = lambda x: abs(cos(x)) ** 3

    def alpha(i):
        return (f(xi(i + 1)) - f(xi(i))) / (cos(xi(i + 1)) - cos(xi(i)))

    result = 0.0

    for i in range(1, m):
        result += (alpha(i-1) - alpha(i)) * sin(xi(i)) * cos(k * xi(i))

    return cos(k * x) / k * result

def msum_sincos(k, m, max_k):
    xi = lambda i: pi * i / m

    result = 0.0

    for s in range(1, max_k + 1):
        result += sin(xi(s)) * cos(k * xi(s))

    return result



# maxsum = 0.0
#
# for k in range(m + 1, m + 500):
#     s = msum(k, m)
#     maxsum = max(maxsum, abs(s))
#     print("k = %i, sum = %2.5f" % (k, s))
#
# print("maxsum = %3.5f" % maxsum)

# sum_k=m^2m msum(k,m)

m = 100
N = 10
maxmsum = 0.0
for i in range(N + 1):
    s = sum([msum(k, m, pi * i / N) for k in range(m, 2*m)])
    print("x = %3.4f, msum = %2.5f" % (pi * i / N, s))
    break
    maxmsum = max(maxmsum, abs(s))
print(maxmsum)

# maxsum = 0.0
#
# for k in range(m + 1, m + 500):
#     s = msum_sincos(k, m)
#     maxsum = max(maxsum, abs(s))
#     print("k = %i, sum = %2.5f" % (k, s))
#
# print("maxsum = %3.5f" % maxsum)

# sum_k=m^2m msum_sincos(k,m)
# N = 1000
# for i in range(N + 1):
#     s = sum([msum_sincos(k, m, 0) for k in range(m, 10*m)])
#     print(s)

# m = 100
#
# s = sum([msum_sincos(k, m, m-1) for k in range(m, 7*m)])
# print(s)
