import math
from scipy.fftpack import dct, idct

class FunctionApproximator:
    def __init__(self):
        self.__gridSize = 32

    @property
    def grid_size(self):
        return self.__gridSize

    @grid_size.setter
    def grid_size(self, N):
        if self.power_of_two(N):
            self.__gridSize = N
        else:
            print("Error: N not set. N must be the power of two!")

    def node(self, i, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size
        return (2.0 * i + 1.0) * math.pi / (2.0 * grid_size)

    def get_grid(self, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size

        grid = []

        for i in range(grid_size):
            grid.append(self.node(i, grid_size))

        return grid

    def discretize_function_1d(self, f, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size

        discretized_function = []

        for i in range(grid_size):
            discretized_function.append(f(self.node(i, grid_size)))

        return discretized_function

    def phi(self, k, x):
        if k == 0:
            return 1.0
        else:
            return math.sqrt(2.0) * math.cos(k * x)

    def set_grid_size_as_power_of_two(self, power):
        n = 1
        while power > 1:
            n *= 2
        self.grid_size = n

    # Slow forward 1D Fourier transform

    def calculate_fourier_coefficient_1d_slow(self, coefficient_index, discrete_function, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size
        discretized_phi = self.discretize_function_1d(lambda x: self.phi(coefficient_index, x), grid_size)
        coefficient = 0.0
        for i in range(len(discrete_function)):
            coefficient += discretized_phi[i] * discrete_function[i]
        return coefficient / grid_size

    def calculate_fourier_transform_1d_slow(self, discrete_function, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size
        coefficients = []
        for k in range(len(discrete_function)):
            coefficients.append(self.calculate_fourier_coefficient_1d_slow(k, discrete_function, grid_size))
        return coefficients

    # Slow inverse 1D Fourier transform

    def calculate_function_value_from_fourier_coefficients(self, coefficients, x, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size
        function_value = 0
        for i in range(len(coefficients)):
            function_value += coefficients[i] * self.phi(i, x)
        return function_value

    def calculate_inverse_fourier_transform_1d_slow(self, coefficients, grid_size = -1):
        if grid_size == -1:
            grid_size = self.grid_size
        function_values = []
        for i in range(len(coefficients)):
            function_values.append(self.calculate_function_value_from_fourier_coefficients(coefficients, self.node(i, grid_size), grid_size))
        return function_values

    @staticmethod
    def power_of_two(n):
        if n < 0:
            n = -n
        while n > 1:
            (d, m) = divmod(n, 2)
            if m == 0:
                n = d
            else:
                return False
        return True

