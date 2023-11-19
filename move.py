


class Move:

    pieces = ['', 'p', 'kn', 'b', 'r', 'q', 'k']

    #def __init__(self, start: tuple[int, int], dest: tuple[int, int], , time: int = 0):
    def __init__(self, start: tuple[int, int], dest: tuple[int, int], flags = None):
        self.start = start
        self.dest = dest
        if flags != None:
            self.flags = flags
        else:
            self.flags = {}


    def from_int(move_num: int):

        # flag_num, position_num = move_num & 0xfffffffffffff000, move_num & 0x0000000000000fff
        flags = {}

        # flags, time = flags & 0xfff0000000000, flags & 0x000ffffffffff
        temp = None
        move_num, temp = divmod(move_num, 2)
        flags['end'] = bool(temp)

        move_num, temp = divmod(move_num, 4)
        flags['end_state'] = ['', 'w', 'd', 'b'] [temp]

        move_num, temp = divmod(move_num, 2)
        flags['check'] = bool(temp)

        move_num, temp = divmod(move_num, 8)
        flags['piece'] = Move.pieces[temp]

        move_num, temp = divmod(move_num, 2)
        flags['promotion'] = bool(temp)

        move_num, temp = divmod(move_num, 8)
        flags['promotion_piece'] = 




        
        

        




        move = [[0, 0], [0, 0]]
        move_position, move[0][0] = divmod(move_position, 8)
        move_position, move[0][1] = divmod(move_position, 8)
        move_position, move[1][0] = divmod(move_position, 8)
        move_position, move[1][1] = divmod(move_position, 8)
        
        # flags = flag_dict[move_num]
        

        move[0][0] += 1
        move[0][1] += 1
        move[1][0] += 1
        move[1][1] += 1

        #return Move(tuple(move[0]), tuple(move[1]), flags)

    def from_bytes(_bytes: bytes):
        
        return Move.from_int(int.from_bytes(_bytes, 'little'))

    
    def to_int(self) -> int:
        flag_dict = {tuple(): 0,
            ('WIN',): 1,
            ('DRAW',): 2,
            ('TIMEOUT',): 3,
            ('TAKE',): 4,
            ('QS_CASTLE',): 5,
            ('KS_CASTLE',): 6,
            ('KNIGHT',): 7,
            ('BISHOP',): 8,
            ('ROOK',): 9,
            ('QUEEN',): 10,
            ('TAKE', 'KNIGHT'): 11,
            ('TAKE', 'BISHOP'): 12,
            ('TAKE', 'ROOK'): 13,
            ('TAKE', 'QUEEN'): 14}
        
        #move has two tuples with x and y from 1 to 8
        move_num = (self.start[0] - 1)
        move_num += (self.start[1] - 1) * (2 ** 3)
        move_num += (self.dest[0] - 1) * (2 ** 6)
        move_num += (self.dest[1] - 1) * (2 ** 9)
        move_num += flag_dict[self.flags] * (2 ** 12)

        return move_num
    
    def to_bytes(self) -> bytes:
        
        return self.to_int().to_bytes(2, 'little')
    
    def __str__(self):
        
        flag_str = ' ' + '|'.join(self.flags)
        if self.piece:
            return f'{self.piece} @ {self.start} -> {self.dest}{flag_str}'
        else:
            return f'{self.start} -> {self.dest}{flag_str}'



if __name__ == '__main__':
    x = Move((8, 8), (2, 2), ('WIN',))
    num = x.to_int()
    print (num)
    print (Move.from_int(num))
    