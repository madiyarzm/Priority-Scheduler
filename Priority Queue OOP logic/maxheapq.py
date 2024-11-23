class MaxHeapq:
    """ 
    A class that implements properties and methods 
    that support a max priority queue data structure

    Attributes
    ----------
    heap : list
        A Python list where key values in the max heap are stored
    heap_size: int
        An integer counter of the number of keys present in the max heap
    """  

    def __init__(self):    
        """
        Parameters
        ----------
        None
        """    
        self.heap = []
        self.heap_size = 0
        
    def left(self, i):
        """ Returns the index of the left child node """
        return 2 * i + 1

    def right(self, i):
        """ Returns the index of the right child node """
        return 2 * i + 2
		
    def parent(self, i):
        """ Returns the index of the parent node """
        return (i - 1) // 2

    def maxk(self):     
        """ Returns the highest key in the priority queue """
        if self.heap_size == 0:
            raise ValueError("Heap is empty")
        return self.heap[0]         
  
    def heappush(self, key):  
        """
        Inserts a key into the priority queue and maintains the max heap property.
        """
        # Increase heap size and append a dummy value to maintain structure
        self.heap.append(-float("inf"))
        self.increase_key(self.heap_size, key)
        self.heap_size += 1
        
    def increase_key(self, i, key): 
        """
        Modifies the value of a key in a max priority queue with a higher value.
        """
        if key < self.heap[i]:
            raise ValueError('New key is smaller than the current key')
        self.heap[i] = key
        # Move up the heap to maintain max-heap property
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            j = self.parent(i)
            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
            i = j    
       
    def heapify(self, i):
        """
        Ensures the subtree rooted at index i satisfies the max heap property.
        """
        l = self.left(i)
        r = self.right(i)
        largest = i
        if l < self.heap_size and self.heap[l] > self.heap[i]:
            largest = l
        if r < self.heap_size and self.heap[r] > self.heap[largest]:
            largest = r
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify(largest)

    def heappop(self):
        """
        Returns and removes the largest key in the max priority queue.
        """
        if self.heap_size < 1:
            raise ValueError('Heap underflow: No keys in the priority queue')
        maxk = self.heap[0]
        # Move the last element to the root and reduce the heap size
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heap_size -= 1
        # Restore the max-heap property
        if self.heap_size > 0:
            self.heapify(0)
        return maxk

    def __str__(self):
        """ String representation of the heap for debugging purposes """
        return f"MaxHeap({self.heap[:self.heap_size]})"

heap = MaxHeapq()

heap.heappush(5)
heap.heappush(10)
heap.heappush(3)
heap.heappush(8)


