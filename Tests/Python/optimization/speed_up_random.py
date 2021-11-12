# Require
import random
from numba import njit, prange


@njit
def seed(a):
    random.seed(a)


@njit
def rand():
    return random.random()


# Return a random integer N such that a <= N <= b
@njit
def randint(a, b):
    return random.randint(a, b)


# Usage
seed(1234)