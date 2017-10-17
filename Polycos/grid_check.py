from math import pi, cos, sin

def f(i, m):
    return abs(cos(pi * i / m) - cos(pi * (i+1) / m))

for m in range(2, 20):
    print("*********** m = %i ************" % m)
    for i in range(m):
        print("(%i) %f < %f" % (f(i,m) < pi / m, f(i,m), pi / m))