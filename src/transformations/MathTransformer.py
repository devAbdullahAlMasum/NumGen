import random
import math
from typing import List

class MathTransformer:
    def __init__(self):
        self.primes = [17, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 3571, 4909]
        # Calculate golden ratio (phi) = (1 + sqrt(5))/2
        golden_ratio = (1 + math.sqrt(5)) / 2
        self.constants = [
            math.pi,    # π (pi)
            math.e,     # e (euler's number)
            math.sqrt(2),  # √2
            golden_ratio,  # φ (phi - golden ratio)
            math.tau,   # τ (tau - 2π)
            math.sqrt(3)   # √3
        ]

    def transform(self, number: int) -> int:
        # Apply multiple layers of transformations
        number = self._prime_transform(number)
        number = self._trigonometric_transform(number)
        number = self._exponential_transform(number)
        number = self._logarithmic_transform(number)
        number = self._constant_transform(number)
        return abs(int(number))

    def _prime_transform(self, number: int) -> float:
        # Apply modulus operations with multiple random primes
        for _ in range(random.randint(2, 4)):
            prime1 = random.choice(self.primes)
            prime2 = random.choice(self.primes)
            number = (number % prime1) * (number % prime2)
        return number

    def _trigonometric_transform(self, number: float) -> float:
        # Apply trigonometric transformations
        operations = [
            lambda x: math.sin(x) * 1000,
            lambda x: math.cos(x) * 1000,
            lambda x: math.tan(x % (math.pi/2)) * 500,
            lambda x: math.sinh(x % 2) * 300,
            lambda x: math.cosh(x % 2) * 300
        ]
        return random.choice(operations)(number)

    def _exponential_transform(self, number: float) -> float:
        # Apply exponential and root transformations
        base = random.uniform(1.1, 2.0)
        power = random.uniform(0.1, 3.0)
        try:
            return pow(abs(number * base), power)
        except OverflowError:
            return pow(abs((number % 100) * base), power)

    def _logarithmic_transform(self, number: float) -> float:
        # Apply logarithmic transformation
        if number <= 0:
            number = 1
        try:
            return math.log(number, random.uniform(2, 10)) * 1000
        except ValueError:
            return math.log(abs(number) + 1, random.uniform(2, 10)) * 1000

    def _constant_transform(self, number: float) -> float:
        # Mix with mathematical constants
        constant = random.choice(self.constants)
        operations = [
            lambda x, c: x * c,
            lambda x, c: x + c,
            lambda x, c: x * c + c,
            lambda x, c: (x + c) * c,
            lambda x, c: (x * c) % (c * 1000)
        ]
        try:
            return random.choice(operations)(number, constant)
        except OverflowError:
            # If overflow occurs, use modulo to bring number into manageable range
            return random.choice(operations)(number % 1000, constant)
