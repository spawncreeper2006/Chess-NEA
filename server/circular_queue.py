
class Circular_Queue:

    def __init__(self, max_size):
        self.data = [''] * max_size
        self.max_size = max_size
        self.data_size = 0
        self.start = 0
        self.end = 0

    def increment(self, x):
        return (x + 1) % self.max_size
    
    def decrement(self, x):
        return (x - 1) % self.max_size
    
    def is_full(self):
        if self.data_size == self.max_size:
            return True
        else:
            return False
        
    def is_empty(self):
        if self.data_size == 0:
            return True
        else:
            return False
    

    def enqueue(self, to_enqueue):
        if self.is_full():
            self.data_size -= 1
            raise Exception('cannot enqueue to a full queue')
        self.data_size += 1
        self.data[self.end] = to_enqueue
        self.end = self.increment(self.end)

    def dequeue(self):
        if self.is_empty():
            raise Exception('cannot dequeue from an empty queue')
        
        self.data_size -= 1
        to_return = self.data[self.end]
        self.start = self.increment(self.start)
        return to_return
    
    def dequeue_all(self):

        if self.is_full():
            to_return = self.data[self.start:] + self.data[:self.end]
        elif self.start == self.end:
            to_return = []
        elif self.start < self.end:
            to_return = self.data[self.start: self.end]
        else:
            to_return = self.data[self.start:] + self.data[:self.end]

        self.start = 0
        self.end = 0
        self.size = 0
        return to_return
        

    def __str__(self):
        if self.is_full():
            return str(self.data[self.start:] + self.data[:self.end])
        elif self.start == self.end:
            return str([])
        elif self.start < self.end:
            return str(self.data[self.start: self.end])
        else:
            return str(self.data[self.start:] + self.data[:self.end])
        
if __name__ == '__main__':
    q = Circular_Queue(2)
    q.enqueue('a')
    q.enqueue('b')
    print (q.dequeue_all())

    