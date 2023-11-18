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
            x = self.__array[self.pointer]
            self.pointer -= 1
            return x

    def __str__(self):
        return str(self.__array[:self.pointer])

class Stack:
    def __init__(self, max_size):
        self.max_size = max_size
        self.__array = [''] * max_size
        self.pointer = 0

    def clear(self):
        self.__array = [''] * self.max_size
        self.pointer = 0

    def push(self, to_push):
        if self.pointer == self.max_size:
            raise Exception('cannot push to full stack')
        else:
            self.__array[self.pointer] = to_push
            self.pointer += 1

    def pop(self):
        if self.pointer == 0:
            raise Exception('cannot pull from empty stack')
        else:
            self.pointer -= 1
            x = self.__array[self.pointer]
            return x
        
    def __str__(self):
        return str(self.__array[:self.pointer])


class NP_Stack:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.__array = np.zeros(max_size, 'int16')
        self.__pointer = 0

    def is_full(self) -> bool:
        return self.__pointer == self.max_size
    
    def is_empty(self) -> bool:
        return self.__pointer == 0
    


    def push(self, move_num: int):
        if self.is_full():
            raise Exception('cannot push to a full stack')
        else:
            self.__array[self.__pointer] = move_num
            self.__pointer += 1

    def peek(self) -> int:
        if self.is_empty():
            raise Exception('cannot peek an empty stack')
        return self.__array[self.__pointer - 1]

    def pop(self) -> int:
        if self.is_empty():
            raise Exception('cannot pop from an empty stack')
        else:
            self.__pointer -= 1
            return self.__array[self.__pointer]
        
    def __str__(self):
        return str(self.__array[:self.__pointer])

stack = Stack(1000)