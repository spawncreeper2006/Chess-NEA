
from typing import Literal

def write_bits(data: int, to_write: int, start: int, max_bit_length: int) -> int:

    if len(bin(to_write)[2:]) > max_bit_length:
        raise ValueError(f'cannot convert {to_write} to bits of length {max_bit_length}')
    
    if (2 ** (start + max_bit_length) - 2 ** (start)) & data:
        raise ValueError('cannot overwrite data with new bits')
    
    return data + 2 ** start * to_write

def write_bool(data: int, _bool: bool, position: int) -> int:
    if data & (2 ** position):
        raise ValueError('cannot overwrite data with new bits')
    return data + int(_bool) * 2 ** position


def read_bits(data: int, start: int, length: int) -> int:
    return ((2 ** (start + length) - 2 ** (start)) & data) >> start

def read_bool(data: int, position: int) -> bool:
    return bool(2 ** position & data)


class Move:

    pieces = ['', 'p', 'kn', 'b', 'r', 'q', 'k']

    #def __init__(self, start: tuple[int, int], dest: tuple[int, int], , time: int = 0):
    def __init__(self, start: tuple[int, int],
                 dest: tuple[int, int],
                 flags: dict = None):
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
            self.flags['take'] = False

    def set_flags(self,
                  end: bool,
                  end_state: str,
                  check: bool,
                  piece: Literal['', 'p', 'kn', 'b', 'r', 'q', 'k'],
                  promotion: bool,
                  promoting_piece: Literal['', 'p', 'kn', 'b', 'r', 'q', 'k'],
                  castling: Literal['', 'QS', 'KS'],
                  take: bool):
        
        self.flags['end'] = end
        self.flags['end_state'] = end_state
        self.flags['check'] = check
        self.flags['piece'] = piece
        self.flags['promotion'] = promotion
        self.flags['promotion_piece'] = promoting_piece
        self.flags['castling'] = castling
        self.flags['take'] = take



    def from_int(move_num: int):


        flags = {}





        flags['end'] = read_bool(move_num, 31)
        flags['end_state'] = ['', 'w', 'd', 'b'] [read_bits(move_num, 29, 2)]
        flags['check'] = read_bool(move_num, 27)
        flags['piece'] = Move.pieces[read_bits(move_num, 24, 3)]
        flags['promotion'] = read_bool(move_num, 23)
        flags['promotion_piece'] = Move.pieces[read_bits(move_num, 20, 3)]
        flags['castling'] = ['', 'QS', 'KS'] [read_bits(move_num, 18, 2)]
        flags['take'] = read_bool(move_num, 16)



        move = [((move_num & 0x00000007) + 1, ((move_num & 0x00000038) >> 3) + 1),
                ( ((move_num & 0x000001c0) >> 6) + 1, ((move_num & 0x00000e00) >> 9) + 1)]
        
        return Move(tuple(move[0]), tuple(move[1]), flags)

    def from_bytes(_bytes: bytes):
        
        return Move.from_int(int.from_bytes(_bytes, 'little'))

    
    def to_int(self) -> int:


        move_num = 0



        move_num = write_bool(move_num, self.flags['end'], 31)

        move_num = write_bits(move_num, to_write=['', 'w', 'd', 'b'].index(self.flags['end_state']), start=29, max_bit_length=2)

        move_num = write_bool(move_num, self.flags['check'], 27)

        move_num = write_bits(move_num, to_write=Move.pieces.index(self.flags['piece']), start=24, max_bit_length=3)

        move_num = write_bool(move_num, self.flags['promotion'], 23)


        move_num = write_bits(move_num, to_write=Move.pieces.index(self.flags['promotion_piece']), start=20, max_bit_length=3)

        move_num = write_bits(move_num, to_write=['', 'QS', 'KS'].index(self.flags['castling']), start=18, max_bit_length=2)

        move_num = write_bool(move_num, self.flags['take'], 16)


        # bits 10 - 17 are redundant

        
        #storing move in move_num
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


    move = Move((1, 1), (2, 2))
    move.set_flags(end=True,
                   end_state='',
                   check=False,
                   piece='kn',
                   promotion=True,
                   promoting_piece='p',
                   castling='QS',
                   take=False)

    num = move.to_int()
    print (Move.from_int(num).flags)