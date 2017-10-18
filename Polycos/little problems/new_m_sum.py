from math import pi, cos, sin

def msum(m,s):
    sum = 0.0
    for i in range(m):
        if (1 - (-1) ** (i + s*m)) != 0:
            sum += 1.0 / ((i + s*m + 1) * (i + s*m)) * 2 / abs(sin(i * pi / (2 * m) + s * pi / 2))

    return sum

for s in range(1,6):
    print("*********** s = %i ************" % (s))
    for m in range(1, 30):
        print("(m = %10.i)\t\t\t\t\t msum = %1.20f" % (2 ** m, msum(2 ** (m+1), s) / msum(2 ** m, s)))

# def msum_simple(m):
#     sum = 0.0
#     for k_ in range(1, m):
#         sum += 1 / abs(sin(k_ * pi / (2 * m)))
#     return sum
#
# for s in range(1,6):
#     print("*********** s = %i ************" % (s))
#     for m in range(1, 8):
#         print("(m = %10.i)\t\t\t\t\t msum = %1.20f" % (10 ** m,  msum_simple(10 ** m)))