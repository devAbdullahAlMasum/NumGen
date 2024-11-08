from collections import deque
import random

class CustomDeque:
    def __init__(self):
        self.deque = deque()

    def append(self, value: int):
        self.deque.append(value)

    def appendleft(self, value: int):
        self.deque.appendleft(value)

    def pop(self) -> int:
        return self.deque.pop()

    def popleft(self) -> int:
        return self.deque.popleft()

    def get_middle(self) -> int:
        """Get an element from the middle section"""
        mid = len(self.deque) // 2
        return list(self.deque)[mid]

    def shuffle(self):
        """Shuffle the deque contents"""
        items = list(self.deque)
        random.shuffle(items)
        self.deque.clear()
        self.deque.extend(items)
