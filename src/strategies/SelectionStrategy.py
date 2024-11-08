import random
from typing import List
from src.structures.MinHeap import MinHeap
from src.structures.MaxHeap import MaxHeap
from src.structures.CustomDeque import CustomDeque

class SelectionStrategy:
    def __init__(self):
        self.pick_count = 0

    def select_candidates(self, deque: CustomDeque, min_heap: MinHeap, max_heap: MaxHeap) -> List[int]:
        candidates = []

        # Get 1-2 numbers from beginning
        candidates.append(deque.deque[0])
        if random.random() < 0.5:
            candidates.append(deque.deque[1])

        # Get 1-2 numbers from end
        candidates.append(deque.deque[-1])
        if random.random() < 0.5:
            candidates.append(deque.deque[-2])

        # Get 1-2 numbers from middle
        candidates.append(deque.get_middle())

        # Get 1-2 random numbers
        candidates.append(random.choice(list(deque.deque)))

        self.pick_count += 1
        return candidates
