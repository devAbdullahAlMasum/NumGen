import random

class BitwiseTransformer:
    def transform(self, number: int) -> int:
        operations = [
            self._xor_transform,
            self._shift_transform,
            self._and_transform,
            self._or_transform,
            self._rotate_transform,
            self._swap_bits_transform,
            self._reverse_bits_transform
        ]

        # Apply 2-5 random transformations
        for _ in range(random.randint(2, 5)):
            operation = random.choice(operations)
            number = operation(number)

        return number

    def _xor_transform(self, number: int) -> int:
        return number ^ random.getrandbits(64)

    def _shift_transform(self, number: int) -> int:
        shift = random.randint(1, 8)
        direction = random.choice(['left', 'right'])
        return (number << shift) if direction == 'left' else (number >> shift)

    def _and_transform(self, number: int) -> int:
        return number & random.getrandbits(64)

    def _or_transform(self, number: int) -> int:
        return number | random.getrandbits(32)

    def _rotate_transform(self, number: int) -> int:
        bits = 64
        rotation = random.randint(1, 63)
        return ((number << rotation) | (number >> (bits - rotation))) & ((1 << bits) - 1)

    def _swap_bits_transform(self, number: int) -> int:
        pos1 = random.randint(0, 31)
        pos2 = random.randint(0, 31)
        bit1 = (number >> pos1) & 1
        bit2 = (number >> pos2) & 1
        x = (bit1 ^ bit2)
        x = (x << pos1) | (x << pos2)
        return number ^ x

    def _reverse_bits_transform(self, number: int) -> int:
        result = 0
        for i in range(32):
            result = (result << 1) | (number & 1)
            number >>= 1
        return result
