import numpy as np

class Coord_Stack:
    def __init__(self, max_size):
        self.max_size = max_size
        self.__array = np.zeros((self.max_size, 2), 'uint8')
        self.pointer = 0

    def push(self, to_push: list[int, int]) -> None:
        if self.pointer == self.max_size:
            raise Exception('Cannot push to full coordinate stack')
        else:
            self.__array[self.pointer] = to_push
            self.pointer += 1
        
    def pop(self) -> list[int, int]:
        if self.pointer == 0:
            raise Exception('Cannot pull from empty coordinate stack')

        else:
            x = self.__data[self.pointer]
            self.pointer -= 1
            return x

    def __str__(self):
        return str(self.__array[:self.pointer])
