import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math
from FunctionApproximator import FunctionApproximator

# 2D function K
def k(x, y):
    return math.cos(x) * math.cos(y)


# 1D function f
def f(x):
    return math.cos(x)

fa = FunctionApproximator()

fa.grid_size = 64

plt.figure(1)
discrete_function = fa.discretize_function_1d(f)
plt.plot(fa.get_grid(), discrete_function)
coefficients = fa.calculate_fourier_transform_1d_slow(discrete_function)
restored_discrete_function = fa.calculate_inverse_fourier_transform_1d_slow(coefficients)
plt.plot(fa.get_grid(), restored_discrete_function)

plt.figure(2)
plt.plot(coefficients, marker='o')

plt.show()
