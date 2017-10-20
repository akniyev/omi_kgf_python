from math import sin, cos, pi

# Estimate of sum_i=1^m-1 (alpha_i-1 - alpha_i)sinxi coskxi for different m and k

def msum(m, k):
    xi = lambda i: pi * i / m
    f = lambda x: abs(cos(x)) ** 3

    def alpha(i):
        return (f(xi(i + 1)) - f(xi(i))) / (cos(xi(i + 1)) - cos(xi(i)))

    values = [(alpha(i-1) - alpha(i)) * sin(xi(i)) * cos(k * xi(i)) for i in range(1, m)]

    return sum(values)

# for m in [10, 100, 1000]:
#     values_for_k = [msum(m, k) for k in range(m + 1, 2 * m)]
#     print("m = %5i, max_msum = %20.15f" % (m, max(values_for_k)))

# Estimate sum_k=m+1^M msum
for m in [10, 50, 100]:
    values_for_k = [abs(msum(m, k)) for k in range(m + 1, 10 * m)]
    print("m = %5i, max_msum = %20.15f" % (m, sum(values_for_k)))

# Estimate sum_k=m+1^M |msum|
for m in [10, 50, 100]:
    values_for_k = [msum(m, k) for k in range(m + 1, 10 * m)]
    print("m = %5i, max_msum = %20.15f" % (m, sum(values_for_k)))