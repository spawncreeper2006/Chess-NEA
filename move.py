


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
            self.flags['end'] = False
            self.flags['end_state'] = ''
            self.flags['check'] = False
            self.flags['piece'] = ''
            self.flags['promotion'] = False
            self.flags['promotion_piece'] = ''
            self.flags['castling'] = ''


    def from_int(move_num: int):

        print (bin(move_num)[2:].zfill(32))

        # # flag_num, position_num = move_num & 0xfffffffffffff000, move_num & 0x0000000000000fff
        flags = {}

        # # flags, time = flags & 0xfff0000000000, flags & 0x000ffffffffff
        # temp = None

        # move_num, temp = divmod(move_num, 2) #1 bit
        # flags['end'] = bool(temp)

        # move_num, temp = divmod(move_num, 4) #2 bits
        # flags['end_state'] = ['', 'w', 'd', 'b'] [temp]

        # move_num, temp = divmod(move_num, 2) #1 bit
        # flags['check'] = bool(temp)

        # move_num, temp = divmod(move_num, 8) #3 bits
        # flags['piece'] = Move.pieces[temp]

        # move_num, temp = divmod(move_num, 2) #1 bit
        # flags['promotion'] = bool(temp)

        # move_num, temp = divmod(move_num, 8) #3 bits
        
        # flags['promotion_piece'] = Move.pieces[temp]

        # move_num, temp = divmod(move_num, 4) #2 bits
        # flags['castling'] = ['', 'QS', 'KS']

        # #cum 13 bits / 32. 19 remaining
        
        # #7 redundant bits :(

        # #12 bits required for move

        print (move_num, move_num & 0x80000000)
        flags['end'] = bool(move_num & 0x80000000)
        flags['end_state'] = ['', 'w', 'd', 'b'] [(move_num & 0x60000000) >> 29]
        flags['check'] = bool(move_num & 0x10000000)
        flags['piece'] = Move.pieces[(move_num & 0x0e000000) >> 25]
        flags['promotion_piece'] = bool(move_num & 0x01000000)
        flags['castling'] = ['', 'QS', 'KS'] [(move_num & 0x00c00000) >> 22]

        #print (move_num & 0x00000d00, move_num, 0x00000100)
        
        # move = [((move_num & 0x00000e00) >> 8 + 1, (move_num & 0x000001c0) >> 5 + 1),
        #         ((move_num & 0x00000038) + 1, (move_num & 0x00000007) + 1)]
        

        move = [((move_num & 0x00000007) + 1, ((move_num & 0x00000038) >> 3) + 1),
                ( ((move_num & 0x000001c0) >> 6) + 1, ((move_num & 0x00000e00) >> 9) + 1)]
        
        return Move(tuple(move[0]), tuple(move[1]), flags)

    def from_bytes(_bytes: bytes):
        
        return Move.from_int(int.from_bytes(_bytes, 'little'))

    
    def to_int(self) -> int:


        move_num = 0

        if self.flags['end'] == True:
            move_num += 2 ** 32

        
        move_num += 2 ** 30 * (['', 'w', 'd', 'b'].index(self.flags['end_state']))

        if self.flags['check'] == True:
            move_num += 2 ** 28

        move_num += 2 ** 26 * (Move.pieces.index(self.flags['piece']))

        if self.flags['promotion'] == True:
            move_num += 2 ** 25

        
        move_num += 2 ** 22 * (['', 'w', 'd', 'b'].index(self.flags['promotion_piece']))

        move_num += 2 ** 20 * (['', 'QS', 'KS'].index(self.flags['castling']))

        

        move_num += (self.start[0] - 1)
        move_num += (self.start[1] - 1) * (2 ** 3)
        move_num += (self.dest[0] - 1) * (2 ** 6)
        move_num += (self.dest[1] - 1) * (2 ** 9)



        return move_num
    
    def to_bytes(self) -> bytes:
        
        return self.to_int().to_bytes(2, 'little')
    
    def __str__(self):
        
        return f'{self.flags["piece"]} @ {self.start} -> {self.dest}'



if __name__ == '__main__':

    # x = Move((2, 3), (4, 5))
    # x.flags['check'] = True
    # print (x)
    # y = x.to_int()
    # print (y)
    # print (Move.from_int(y))

    x = Move((2, 3), (4, 5))
    x.flags['end'] = True
    x.flags['check'] = True
    y = x.to_int()
    print (Move.from_int(y).flags)
