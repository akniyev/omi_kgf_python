from math import *
from scipy.fftpack import dct, idct
import numpy as np
from typing import *

def fourierCoefficientsForEvenFunction(f: Callable[[float], float], n: int, discretization: int = 50000) -> List[float]:
    N = discretization
    xs = [pi * i / (N - 1) for i in range(N)]
    ys = [f(xs[i]) for i in range(N)]
    coefficients = [c / N for c in dct(ys)]
    coefficients[0] /= 2
    return coefficients[:n+1]

def fourierCoefficientsForEvenFunctionPreCalculated(ys: List[float], n: int, discretization: int = 50000) -> List[float]:
    N = discretization
    xs = [pi * i / (N - 1) for i in range(N)]
    coefficients = [c / N for c in dct(ys)]
    coefficients[0] /= 2
    return coefficients[:n+1]

def functionFromCoefficientsForEvenFunction(coefficients: List[float], discretization: int = 5000) -> Tuple[List[float], List[float]]:
    N = discretization
    n = len(coefficients)
    coefficients = coefficients[:]
    coefficients.extend([0] * (N - n))
    coefficients[0] *= 2
    coefficients = [c/2 for c in coefficients]

    xs = [pi * i / (N - 1) for i in range(N)]
    ys = idct(coefficients)

    return (xs, ys)



#print(fourierCoefficientsForEvenFunction(lambda x: cos(x) + 1, 5))

