import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from math import *
from mpl_toolkits.mplot3d import Axes3D
import numpy

from FunctionApproximator import FunctionApproximator


plt.ioff()


# 2D function K
def k(x, y):
    return 1.0 / sqrt(fabs(x-y) + 0.01)
    # return sqrt(fabs(x - y)) + 0.01
    # function_sum = 0
    # n = 10
    # for s in range(n+1):
    #     for l in range(s+1):
    #         function_sum += cos((s-l)*x)*cos(l*y)/(((s+1) ** 2) * ((s-l+1) ** 2))
    #
    # return function_sum
    # return sqrt(x) + sqrt(y) + 0.01 # 1.0 / (fabs(sin(x)) + fabs(cos(x)) + fabs(sin(y)) + fabs(cos(y)))


# 1D function f
def f(x):
    return cos(x) + cos(3 * x) + cos(2 * x) + 1  # math.sin(1/x + 1) + x


# Printing
def print_1d_array_to_file(array_to_print, filename):
    with open(filename, 'w') as file:
        for item in array_to_print:
            file.write("{:15.10f}".format(item))
        file.write("\n")


def print_2d_array_to_file(array_to_print, filename):
    with open(filename, 'w') as file:
        for row in array_to_print:
            for item in row:
                file.write("\t\t{}".format(item))
            file.write("\n")

#

fa = FunctionApproximator()

fa.grid_size = 256

# Draw 2D function k

x = fa.get_grid()
y = fa.get_grid()

discrete_function_k = fa.discretize_function_2d(k)
# discrete_function_k

hf = plt.figure(1)
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)

ha.plot_surface(X, Y, discrete_function_k, rcount=fa.grid_size, ccount=fa.grid_size)

# Draw coefficients of k

x = fa.get_grid()
y = fa.get_grid()

hf = plt.figure(4)
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)

coefficients_of_k = FunctionApproximator.calculate_fourier_transform_2d_fast(discrete_function_k)
print_2d_array_to_file(coefficients_of_k, "coefficients of K.txt")

ha.plot_wireframe(X, Y, coefficients_of_k, rcount=fa.grid_size, ccount=fa.grid_size)

# Draw restored function k

x = fa.get_grid()
y = fa.get_grid()

restored_discrete_function_k = FunctionApproximator.calculate_inverse_fourier_transform_2d_fast(coefficients_of_k)
restored_discrete_function_k

hf = plt.figure(8)
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)

ha.plot_surface(X, Y, restored_discrete_function_k)

# Draw function f
plt.figure(2)

discrete_function = fa.discretize_function_1d(f)
plt.plot(fa.get_grid(), discrete_function)

# Calculate and draw coefficients of f
coefficients_of_f = FunctionApproximator.calculate_fourier_transform_1d_fast(discrete_function)
fast_restored_discrete_function = fa.calculate_inverse_fourier_transform_1d_fast(coefficients_of_f)

print_1d_array_to_file(coefficients_of_f, "coefficients_of_f.txt")
plt.plot(fa.get_grid(), fast_restored_discrete_function)

plt.figure(3)
plt.plot(coefficients_of_f, marker='o')

plt.show()
