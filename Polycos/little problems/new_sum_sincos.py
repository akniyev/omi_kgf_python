from math import sin, cos, pi

m = 1000
k = 3000

xi = lambda i: pi * i / m

addends = [sin(xi(i)) * cos(k*xi(i)) for i in range(1, m)]
print(sum(addends))