import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy

from FunctionApproximator import FunctionApproximator


# 2D function K
def k(x, y):
    return x * x * 1.0 / (math.fabs(math.sin(x)) + math.fabs(math.cos(x)) + math.fabs(math.sin(y)) + math.fabs(math.cos(y)))


# 1D function f
def f(x):
    return math.sin(1/x + 1) + x

fa = FunctionApproximator()

fa.grid_size = 1024

# Draw 2D function k

x = fa.get_grid()
y = fa.get_grid()

discrete_function_k = fa.discretize_function_2d(k)
discrete_function_k

hf = plt.figure(1)
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)

ha.plot_surface(X, Y, discrete_function_k)

# Draw coefficients of k

x = fa.get_grid()
y = fa.get_grid()

hf = plt.figure(4)
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)

coefficients_of_k = FunctionApproximator.calculate_fourier_transform_2d_fast(discrete_function_k)

ha.plot_wireframe(X, Y, coefficients_of_k)

# Draw restored function k

x = fa.get_grid()
y = fa.get_grid()

restored_discrete_function_k = FunctionApproximator.calculate_inverse_fourier_transform_2d_fast(coefficients_of_k)
restored_discrete_function_k

hf = plt.figure(1)
ha = hf.add_subplot(111, projection='3d')

X, Y = numpy.meshgrid(x, y)

ha.plot_surface(X, Y, restored_discrete_function_k)

#
plt.figure(2)

discrete_function = fa.discretize_function_1d(f)
plt.plot(fa.get_grid(), discrete_function)

coefficients = fa.calculate_fourier_transform_1d_slow(discrete_function)
fast_coefficients = FunctionApproximator.calculate_fourier_transform_1d_fast(discrete_function)

restored_discrete_function = fa.calculate_inverse_fourier_transform_1d_slow(coefficients)
fast_restored_discrete_function = fa.calculate_inverse_fourier_transform_1d_fast(fast_coefficients)

plt.plot(fa.get_grid(), restored_discrete_function)
plt.plot(fa.get_grid(), fast_restored_discrete_function)

plt.figure(3)
plt.plot(coefficients, marker='o')

plt.plot(fast_coefficients, marker='o')

print(fast_coefficients[0] / coefficients[0])

plt.axes().set_aspect('equal', 'datalim')
plt.show()
