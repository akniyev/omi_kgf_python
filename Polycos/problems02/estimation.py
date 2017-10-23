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

# # Estimate sum_k=m+1^M msum
# for m in [10, 50, 100]:
#     values_for_k = [abs(msum(m, k)) for k in range(m + 1, 10 * m)]
#     print("m = %5i, max_msum = %20.15f" % (m, sum(values_for_k)))

# # Estimate sum_k=m+1^M |msum|
# x = 0.0
# for m in [10, 50, 100]:
#     values_for_k = [msum(m, k) for k in range(m + 1, 10 * m)]
#     print("m = %5i, max_msum = %20.15f" % (m, sum(values_for_k)))

# Estimate sum_k=m+1^M cos kx / k |msum|
# x = pi / 4
# for m in [10, 100, 1000]:
#     values_for_k = [cos(k * x) / k * msum(m, k) for k in range(m + 1, 3 * m)]
#     print("m = %5i, max_msum = %20.15f" % (m, sum(values_for_k)))

def sum_cos_msum(m, k, x):
    xi = lambda i: pi * i / m
    f = lambda x: abs(cos(x)) ** 3

    def alpha(i):
        return (f(xi(i + 1)) - f(xi(i))) / (cos(xi(i + 1)) - cos(xi(i)))

    isum = 0.0
    for i in range(1, m):
        ssum = 0.0
        for s in range(m + 1, k + 1):
            ssum += cos(s * x) * cos(s * xi(i)) / s
        isum += (alpha(i-1) - alpha(i)) * sin(xi(i)) * ssum

    return isum

# N = 10
# x = pi / N * 6
# for m in [10, 100, 1000]:
#     s = sum_cos_msum(m, 3 * m, x)
#     print("m = %5i, max_msum = %20.15f" % (m, s))

# Estimate \sum_{j=1}^{m-1}\sin x_{j}\sum_{s=m+1}^{k}\frac{\cos sx\cos sx_{j}}{s}

def sum_sincoscos(x, m, k, i):
    xi = lambda i: pi * i / m
    return sin(xi(i)) * sum([sin(xi(j)) * sum([cos(s*x) * cos(s*xi(j)) / s for s in range(m+1, k)]) for j in range(1,i+1)])

# N = 10
# for m in [10]:
#     max_sum = 0.0
#     for i in range(m-1, m):
#         for k in range(m+1, 20*m):
#             for x in [pi * i / N for i in range(0, N+1)]:
#                 max_sum = max(max_sum, abs(sum_sincoscos(x, m, k, i)))
#     print("m=%3i, max_sum=%20.15f" % (m, max_sum))

# Estimate alpha_i-1-alpha_i
m = 1000
xi = lambda i: pi * i / m
f = lambda x: abs(cos(2 * x)) ** 2

def alpha(i):
    return (f(xi(i + 1)) - f(xi(i))) / (cos(xi(i + 1)) - cos(xi(i)))

m_diff = 0.0

for i in range(1, m - 2):
    diff = ((alpha(i-1) - alpha(i)) - (alpha(i) - alpha(i+1))) - ((alpha(i) - alpha(i+1)) - (alpha(i+1) - alpha(i+2)))
    m_diff = max(m_diff, abs(diff))
    print("i = %5i, alpha_i-1 - alpha_i = %20.15f" % (i, diff))

print(m_diff)