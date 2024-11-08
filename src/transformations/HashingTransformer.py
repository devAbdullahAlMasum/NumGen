import hashlib
import struct
import random
import hmac

class HashingTransformer:
    def __init__(self):
        self.salt = random.randbytes(16)
        self.keys = [random.randbytes(32) for _ in range(5)]
        self.algorithms = [
            hashlib.sha256,
            hashlib.sha512,
            hashlib.sha3_256,
            hashlib.blake2b,
            hashlib.sha3_512
        ]

    def transform(self, number: int) -> int:
        # Multi-layer hashing
        result = number

        # Apply multiple rounds of hashing
        for _ in range(random.randint(2, 4)):
            result = self._single_hash_round(result)

        # Apply HMAC with random key
        result = self._hmac_round(result)

        # Final mixing
        result = self._mix_bits(result)

        return result

    def _single_hash_round(self, number: int) -> int:
        # Choose random algorithm
        algorithm = random.choice(self.algorithms)

        # Add salt to the input
        input_data = str(number).encode() + self.salt

        # Hash the data
        hashed = algorithm(input_data).digest()

        # Convert to integer
        return int.from_bytes(hashed[:8], byteorder='big')

    def _hmac_round(self, number: int) -> int:
        key = random.choice(self.keys)
        h = hmac.new(key, str(number).encode(), hashlib.sha512)
        return int.from_bytes(h.digest()[:8], byteorder='big')

    def _mix_bits(self, number: int) -> int:
        # Additional bit mixing for more randomness
        number = ((number << 13) ^ number) & ((1 << 64) - 1)
        number = ((number >> 7) ^ number) & ((1 << 64) - 1)
        number = ((number << 17) ^ number) & ((1 << 64) - 1)
        return number
