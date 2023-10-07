


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
    

    def enqueue(self, to_enqueue):
        if self.data_size == self.max_size:
            self.data_size -= 1
            raise Exception('cannot enqueue to a full queue')
        self.data_size += 1
        self.data[self.end] = to_enqueue
        self.end = self.increment(self.end)

    def dequeue(self):
        if self.data_size == 0:
            raise Exception('cannot dequeue from an empty queue')
        
        self.data_size -= 1
        to_return = self.data[self.end]
        self.start = self.increment(self.end)
        return to_return

    def __str__(self):
        start, end = self.start, self.end
        end = self.decrement(end)


        if start <= end:
            return str(self.data[start: end + 1])
        else:
            return str(self.data[start:] + self.data[:end + 1])
        
