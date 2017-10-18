from math import pi, cos, sin

def x(i, m):
    return pi * i / m

for m in range(3, 50):
    print("*********** m = %i ************" % m)
    for i in range(1,m-1):
        print("m = %i, i = %i, sinx_i/sinx_{i+1} = %f)" % (m, i, 1-  sin(x(i, m)) / sin(x(i+1, m))))
        # print("m = %i, i = %i, sinx_i/sinx_{i+1} = %f)" % (m, i, (cos(x(i+1, m)) - cos(x(i-1, m))) / (cos(x(i+2, m)) - cos(x(i,m)))))

