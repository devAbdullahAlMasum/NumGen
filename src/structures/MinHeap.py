class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value: int):
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def get_min(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def extract_min(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty")

        min_val = self.heap[0]
        last_val = self.heap.pop()

        if self.heap:
            self.heap[0] = last_val
            self._sift_down(0)

        return min_val

    def _sift_up(self, index: int):
        parent = (index - 1) // 2

        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index: int):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)
