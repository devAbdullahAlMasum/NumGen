import random
from typing import List, Set

class SegmentedPool:
    def __init__(self, start: int, end: int, segment_count: int):
        self.start = start
        self.end = end
        self.segment_count = segment_count
        self.segments = []
        self.excluded_numbers = set()

        self._create_segments()
        self._create_gaps()

    def _create_segments(self):
        range_size = self.end - self.start + 1
        segment_size = range_size // self.segment_count

        for i in range(self.segment_count):
            segment_start = self.start + (i * segment_size)
            segment_end = segment_start + segment_size - 1
            if i == self.segment_count - 1:
                segment_end = self.end

            self.segments.append((segment_start, segment_end))

    def _create_gaps(self):
        """Create random gaps in each segment"""
        for start, end in self.segments:
            segment_size = end - start + 1
            gap_size = segment_size // 10  # Remove ~10% of numbers

            for _ in range(gap_size):
                while True:
                    num = random.randint(start, end)
                    if num not in self.excluded_numbers:
                        self.excluded_numbers.add(num)
                        break

    def get_all_numbers(self) -> List[int]:
        """Return all numbers that aren't in gaps"""
        numbers = []
        for start, end in self.segments:
            for num in range(start, end + 1):
                if num not in self.excluded_numbers:
                    numbers.append(num)
        return numbers
