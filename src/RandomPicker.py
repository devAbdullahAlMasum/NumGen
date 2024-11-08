from typing import List, Tuple
import random
import statistics
from src.structures.SegmentedPool import SegmentedPool
from src.structures.MinHeap import MinHeap
from src.structures.MaxHeap import MaxHeap
from src.structures.CustomDeque import CustomDeque
from src.transformations.BitwiseTransformer import BitwiseTransformer
from src.transformations.MathTransformer import MathTransformer
from src.transformations.HashingTransformer import HashingTransformer
from src.strategies.SelectionStrategy import SelectionStrategy

class RandomPicker:
    def __init__(self, start: int, end: int, segment_count: int = 5):
        self.start = start
        self.end = end
        self.range = end - start + 1
        self.history = []  # Keep track of generated numbers

        # Initialize data structures with more segments
        self.segmented_pool = SegmentedPool(start, end, segment_count)
        self.min_heap = MinHeap()
        self.max_heap = MaxHeap()
        self.deque = CustomDeque()

        # Initialize transformers
        self.bitwise_transformer = BitwiseTransformer()
        self.math_transformer = MathTransformer()
        self.hash_transformer = HashingTransformer()

        # Initialize selection strategy
        self.selection_strategy = SelectionStrategy()

        # Initialize structures with segmented numbers
        self._initialize_structures()

    def _initialize_structures(self):
        numbers = self.segmented_pool.get_all_numbers()
        for num in numbers:
            self.min_heap.insert(num)
            self.max_heap.insert(num)
            self.deque.append(num)

    def pick(self) -> int:
        # 1. Get candidate numbers using multi-position strategy
        candidates = self.selection_strategy.select_candidates(
            self.deque,
            self.min_heap,
            self.max_heap
        )

        # 2. Apply transformations
        transformed = self._apply_transformations(candidates)

        # 3. Enhanced final number selection
        final_number = self._select_final_number(transformed)

        # 4. Periodic shuffling (every 7 picks instead of 10)
        if self.selection_strategy.pick_count % 7 == 0:
            self.deque.shuffle()

        # 5. Store in history for distribution analysis
        self.history.append(final_number)
        if len(self.history) > 1000:  # Keep history manageable
            self.history.pop(0)

        return final_number

    def _select_final_number(self, transformed: List[int]) -> int:
        # Apply multiple selection strategies
        candidates = []

        # Strategy 1: Basic modulo
        number1 = self.start + (transformed[0] % self.range)
        candidates.append(number1)

        # Strategy 2: Reverse bits then modulo
        number2 = self.start + (self._reverse_bits(transformed[1]) % self.range)
        candidates.append(number2)

        # Strategy 3: XOR all transformed numbers
        xor_result = transformed[0]
        for num in transformed[1:]:
            xor_result ^= num
        number3 = self.start + (xor_result % self.range)
        candidates.append(number3)

        # Strategy 4: Use distribution analysis if history exists
        if self.history:
            least_frequent_regions = self._find_least_frequent_regions()
            number4 = self._generate_number_in_region(least_frequent_regions)
            if number4 is not None:
                candidates.append(number4)

        # Final selection: randomly choose from candidates
        return random.choice(candidates)

    def _reverse_bits(self, n: int) -> int:
        result = 0
        for i in range(64):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result

    def _find_least_frequent_regions(self) -> List[Tuple[int, int]]:
        if not self.history:
            return [(self.start, self.end)]

        # Divide range into 10 regions
        region_size = max(1, self.range // 10)
        regions = []
        counts = [0] * 10

        # Count numbers in each region
        for num in self.history:
            region_index = min(9, (num - self.start) // region_size)
            counts[region_index] += 1

        # Find regions with below-average counts
        avg_count = statistics.mean(counts)
        least_frequent = []

        for i, count in enumerate(counts):
            if count < avg_count:
                region_start = self.start + (i * region_size)
                region_end = min(self.end, region_start + region_size - 1)
                least_frequent.append((region_start, region_end))

        return least_frequent or [(self.start, self.end)]

    def _generate_number_in_region(self, regions: List[Tuple[int, int]]) -> int:
        if not regions:
            return None

        # Select random region and generate number within it
        start, end = random.choice(regions)
        return random.randint(start, end)

    def _apply_transformations(self, numbers: List[int]) -> List[int]:
        transformed = []
        for num in numbers:
            # Apply transformations in random order
            transformers = [
                self.bitwise_transformer.transform,
                self.math_transformer.transform,
                self.hash_transformer.transform
            ]
            random.shuffle(transformers)

            for transformer in transformers:
                num = transformer(num)

            transformed.append(num)

        return transformed
