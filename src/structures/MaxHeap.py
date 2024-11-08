class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value: int):
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def get_max(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def extract_max(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty")

        max_val = self.heap[0]
        last_val = self.heap.pop()

        if self.heap:
            self.heap[0] = last_val
            self._sift_down(0)

        return max_val

    def _sift_up(self, index: int):
        parent = (index - 1) // 2

        if index > 0 and self.heap[index] > self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index: int):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left

        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._sift_down(largest)
