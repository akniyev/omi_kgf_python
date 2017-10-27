from math import sin, cos, pi
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication

# It calculates the sum
# \sum_{i=1}^{m-1}\left(\alpha_{i-1}-\alpha_{i}\right)\sin x_{i}\cos kx_{i} \cos kx / k
def msum(k, m):
    xi = lambda i: pi * i / m
    f = lambda x: abs(cos(x)) ** 3

    def alpha(i):
        return (f(xi(i + 1)) - f(xi(i))) / (cos(xi(i + 1)) - cos(xi(i)))

    result = 0.0

    for i in range(1, m):
        result += (alpha(i-1) - alpha(i)) * sin(xi(i)) * cos(k * xi(i))

    return result

def sum_msum(m, max_k):
    xi = lambda i: pi * i / m
    f = lambda x: abs(cos(x)) ** 3

    def alpha(i):
        return (f(xi(i + 1)) - f(xi(i))) / (cos(xi(i + 1)) - cos(xi(i)))

    ssum = 0.0
    for s in range(m + 1, max_k + 1):
        isum = 0.0
        for i in range(1, m):
            isum += (alpha(i - 1) - alpha(i)) * sin(xi(i)) * cos(s * xi(i))
        ssum += isum

    return ssum
    # result = 0.0
    #
    # for i in range(1, m):
    #     result += (alpha(i-1) - alpha(i)) * sin(xi(i)) / sin(xi(i) / 2) * (sin((2 * k + 1) / 2 * xi(i)) - sin((2 * m + 1) / 2 * xi(i)))

def msum_sincos(k, m, max_k):
    xi = lambda i: pi * i / m

    result = 0.0

    for s in range(1, max_k + 1):
        result += sin(xi(s)) * cos(k * xi(s))

    return result

# \sum_{s=1}^{i}\sin x_{s}\cos kx_{s}
def s_sum_sinxcossx(i, k, m):
    xi = lambda i: pi * i / m
    ssum = 0.0
    for s in range(1, i + 1):
        ssum += sin(xi(s)) * cos(k * xi(s))

    return ssum


for m in [10, 100, 1000, 10000]:
    for k in range(2 * m - 2, 2 * m):
        print("k = %4i" % k)
        maxs = 0.0
        for i in range(1, m):
            s = s_sum_sinxcossx(i, k, m)
            maxs = max(maxs, abs(s))
            # print("(i = %5i) s = %10.6f" % (i, s))
        print("m = %5i, i = 1,..,%i, max_s = %10.5f" % (m, m-1, maxs))




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
# maxmsum = 0.0
# for i in range(N + 1):
#     s = sum([msum(k, m, pi * i / N) for k in range(m, 2*m)])
#     print("x = %3.4f, msum = %2.5f" % (pi * i / N, s))
#     break
#     maxmsum = max(maxmsum, abs(s))
# print(maxmsum)

m = 10
maxmsum = 0.0
for max_k in range(m + 1, 2 * m):
    s = sum([msum(k, m) for k in range(m, max_k + 1)])
    s1 = sum_msum(m, max_k)
    #print("k = %4i to %4i, msum = %18.13f / %18.13f, current_max = %18.13f" % (m, max_k, s, s1, maxmsum))
    maxmsum = max(maxmsum, abs(s))
print("max = %10.5f" % maxmsum)

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

# m = 1000
#
# for k in range(m + 1, 2 * m):
#     print(sum_msum(m, k))