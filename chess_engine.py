
from copy import deepcopy
from stack import stack, NP_Stack


KNIGHT_VECTORS = [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1), (1, 2), (-1, 2)]
ROOK_VECTORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
BISHOP_VECTORS = [(1, 1), (-1,-1), (-1, 1), (1, -1)]
QUEEN_VECTORS = ROOK_VECTORS + BISHOP_VECTORS
KING_VECTORS = QUEEN_VECTORS

BLACK_WOOD = (145, 60, 26)
WHITE_WOOD = ( 245, 219, 135)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SEP = "==============================================="
sep = lambda: print(SEP)



def in_board(pos: tuple) -> bool:
    for xy in pos:
        if xy < 1 or xy > 8:
            return False

    return True



class Move:

    def __init__(self, start: tuple[int, int], dest: tuple[int, int], flags: tuple = (), board = None):
        self.start = start
        self.dest = dest
        self.flags = flags
        self.piece = ''
        if board != None:
            self.piece = board.coords(start).piece.piece_identifier


    def from_int(move_num: int):
        flag_dict = {0: (),
            1: ('WIN'),
            2: ('DRAW'),
            3: ('TIMEOUT'),
            4: ('TAKE'),
            5: ('QS_CASTLE'),
            6: ('KS_CASTLE'),
            7: ('KNIGHT'),
            8: ('BISHOP'),
            9: ('ROOK'),
            10: ('QUEEN'),
            11: ('TAKE', 'KNIGHT'),
            12: ('TAKE', 'BISHOP'),
            13: ('TAKE', 'ROOK'),
            14: ('TAKE', 'QUEEN')}
        
        
        move = [[0, 0], [0, 0]]

        move_num, move[0][0] = divmod(move_num, 8)
        move_num, move[0][1] = divmod(move_num, 8)
        move_num, move[1][0] = divmod(move_num, 8)
        move_num, move[1][1] = divmod(move_num, 8)
        flags = flag_dict[move_num]

        move[0][0] += 1
        move[0][1] += 1
        move[1][0] += 1
        move[1][1] += 1

        return Move(tuple(move[0]), tuple(move[1]), flags)

    def from_bytes(_bytes: bytes):
        
        return Move.from_int(int.from_bytes(_bytes, 'little'))

    
    def to_int(self) -> int:
        flag_dict = {(): 0,
            ('WIN'): 1,
            ('DRAW'): 2,
            ('TIMEOUT'): 3,
            ('TAKE'): 4,
            ('QS_CASTLE'): 5,
            ('KS_CASTLE'): 6,
            ('KNIGHT'): 7,
            ('BISHOP'): 8,
            ('ROOK'): 9,
            ('QUEEN'): 10,
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
        if self.piece:
            return f'{self.piece} @ {self.start} -> {self.dest}'
        else:
            return f'{self.start} -> {self.dest}'

    


def get_team_moves(team: str, this_board):
    moves = []
    team_pieces = []
    match team:
        case 'w':
            team_pieces = this_board.white_pieces
        case 'b':
            team_pieces = this_board.black_pieces

    for piece in team_pieces:
        moves = piece.get_moves(this_board)
        for move in moves:
            yield (piece, move)

def get_team_attack_moves(team:str, this_board) -> set:
    
    moves = []
    team_pieces = []
    match team:
        case 'w':
            team_pieces = this_board.white_pieces
        case 'b':
            team_pieces = this_board.black_pieces

    

    for piece in team_pieces:


        moves += piece.get_possible_attack_moves(this_board)


    return set(moves)

def does_not_endanger_king(piece, board, pos) -> bool:
    possible_board = deepcopy(board)
    
    piece_position = piece.pos
    piece = possible_board.coords(piece_position).piece
    possible_board = piece.move(possible_board, pos, is_simulated=True)
    
    enemy_attack_moves = get_team_attack_moves(possible_board.current_turn, possible_board)
    
    return not possible_board.king_pos[other_team(possible_board.current_turn)] in enemy_attack_moves
        


def add_coords(c1:tuple,
               c2:tuple) -> tuple:
    if len(c1) != len(c2):
        raise Exception(f'Unable to add tuples with length {len(c1)} and length {len(c2)}')
    
    return tuple([a + b for a, b in zip(c1, c2)])

def other_team(team:str) -> str:
    match team:
        case 'w':
            return 'b'
        case 'b':
            return 'w'
        
def king_in_check(board):
    if board.king_pos[board.current_turn] in get_team_attack_moves(other_team(board.current_turn), board):
        match board.current_turn:
            case 'w':
                board.white_checked = True
                
            case 'b':
                board.black_checked = True

        return True

    else:
        board.white_checked = False
        board.black_checked = False

    return False

def can_move(board):
    for (piece, move) in get_team_moves(board.current_turn, board):
        if does_not_endanger_king(piece, board, move):
            return True
        
    return False

class Square:
    def __init__(self, color:tuple):
        self.contains_piece = False
        self.piece = None
        self.color = color
        self.default_color = color

    def update_piece(self,
                     piece=None):

        if piece is None:
            self.contains_piece = False
            self.piece = None

        else:
            self.contains_piece = True
            self.piece = piece
        
    

    def clicked(self):
        if self.contains_piece:

            self.color = GREEN
        else:
            pass

    def is_possible_move(self):
        # self.color = BLUE
        pass

    def back_to_default_color(self):
        self.color = self.default_color

    def __str__(self):

        if self.contains_piece:
            return str(self.piece)
        else:
            return ' ' * 4

class Board:
    def __init__(self):

        self.data = []
        self.current_turn = 'w'
        self.white_checked = False
        self.black_checked = False
        self.win_state = ''
        self.white_pieces = []
        self.black_pieces = []
        self.taken_white_pieces = []
        self.taken_black_pieces = []
        self.king_pos = {}
        #self.previous_piece_to_move = None
        #self.previous_move = ()
        #self.previous_move = None
        self.stack = NP_Stack(500)
        


    def change_current_turn(self):
        match self.current_turn:
            case 'w':
                self.current_turn = 'b'
            case 'b':
                self.current_turn = 'w'

    def translate_position(self, pos: tuple) -> tuple:
        pos = (pos[0]-1, pos[1]-1)
        return pos[0]+pos[1]*8

    def in_board(self,
                pos:tuple) -> bool:
        return in_board(pos)

    
    def coords(self, 
               pos:tuple) -> Square:
        
        return self.data[self.translate_position(pos)]
    
    def pos_contains_piece(self,
                           pos:tuple) -> bool:
        return self.coords(pos).contains_piece
    
    def ask_for_promotion(self):
        return Queen
    

    
    def __str__(self):
        ls = [[], [], [], [], [] ,[] ,[] ,[]]

        for count, piece in enumerate(self.data):
            ls[7-count//8].append(str(piece))
        return '\n'.join([''.join(i) for i in ls])
    



class Piece:
    def __init__(self, this_board: Board, color:str, pos:tuple, piece_type:str):

        

        self.color = color
        self.pos = pos
        this_board.coords(pos).update_piece(self)
        self.has_moved = False

        if len(piece_type) == 1:
            piece_type = piece_type.upper()
        else:
            piece_type = piece_type[0].upper() + piece_type[1:]
            
        self.piece_identifier = self.color.upper() + piece_type


        self.pieces = []

        match color:
            case 'w':
                this_board.white_pieces.append(self)
                self.pieces = this_board.white_pieces
            case 'b':
                this_board.black_pieces.append(self)
                self.pieces = this_board.black_pieces


        



    def die(self, new_board:Board):
        self.pieces.remove(self)
        pieces = []
        team = ''
        match self.color:
            case 'w':
                pieces = new_board.taken_white_pieces
                team = 'W'
            case 'b':
                pieces = new_board.taken_black_pieces
                team = 'B'

        match self.piece_identifier[1:]:
            case 'P':
                pieces.insert(0, self.piece_identifier)
            case 'B':
                pieces.insert(pieces.count(team + 'P'), self.piece_identifier)
            case 'Kn':
                pieces.insert(pieces.count(team + 'P') + pieces.count(team + 'B'), self.piece_identifier)
            case 'R':
                pieces.insert(pieces.count(team + 'P') + pieces.count(team + 'B') + pieces.count(team + 'Kn'), self.piece_identifier)
            case 'Q':
                pieces.insert(pieces.count(team + 'P') + pieces.count(team + 'B') + pieces.count(team + 'Kn') + pieces.count(team + 'R'), self.piece_identifier)

        

    def move(self,
             new_board: Board,
             new_pos: tuple,
             is_simulated=False,
             flip_board=True,
             is_computer=False):
        


        # new_board.previous_move = (self.pos, new_pos)
        # new_board.previous_piece_to_move = self
        previous_move = Move(self.pos, new_pos, board=new_board)

        new_board.coords(self.pos).update_piece(None)
        
        target_square = new_board.coords(new_pos)

        if target_square.contains_piece: #killing a piece

            
            target_square.piece.die(new_board)
            target_square.update_piece(self)
        else:
            target_square.update_piece(self)

        if type(self) is Pawn:
            if new_pos == self.en_passant_move:
                square = new_board.coords((new_pos[0], new_pos[1] - self.yvector))
                square.piece.die(new_board)
                square.update_piece(None)

        
        
        old_pos = self.pos
        self.pos = new_pos
        self.has_moved = True
        if flip_board:
            new_board.change_current_turn()

        

        
        if self.piece_identifier[1] == 'P' and (not is_simulated) or is_computer: #it is a pawn

            if abs(old_pos[1] - new_pos[1]) == 2:

                self.double_moved = True
            else:
                self.double_moved = False

            

            to_promote = False
            
            match self.color:
                case 'w':
                     if self.pos[1] == 8:
                         to_promote = True
                         
                         new_board.white_pieces.remove(self)
                         team = 'w'
                case 'b':
                    if self.pos[1] == 1:
                        to_promote = True
                        
                        new_board.black_pieces.remove(self)
                        team = 'b'


            if to_promote:
                if is_computer:
                    new_piece = Queen
                else:
                    new_piece = new_board.ask_for_promotion()

                
                piece = new_piece(new_board, team, self.pos)
                match piece.piece_identifier[1:]:
                    case 'Kn':
                        new_board.previous_move.flag = 'KNIGHT'
                    case 'B':
                        new_board.previous_move.flag = 'BISHOP'
                    case 'R':
                        new_board.previous_move.flag = 'ROOK'
                    case 'Q':
                        new_board.previous_move.flag = 'QUEEN'


        in_check = king_in_check(new_board)

        if not is_simulated:

            cm = can_move(new_board)


            if not cm:

                if in_check:
                    new_board.win_state = other_team(new_board.current_turn)

                else:
                    new_board.win_state = 'd'

        if new_board.win_state != '':
            if new_board.win_state == 'd':
                previous_move.flag = 'DRAW'
            else:
                previous_move.flag = 'WIN'

        new_board.stack.push(previous_move.to_int())

        return new_board

    def same_color(self,
                   color: str) -> bool:
        return self.color==color

    def __str__(self):
        return self.piece_identifier.zfill(4).replace('0', ' ')
    
    def valid_move(self,
                   board,
                   pos:tuple) -> bool:
        if not board.in_board(pos):
            return False
        
        x = board.coords(pos)

        if x.contains_piece:
            if self.same_color(x.piece.color):
                return False

        return True
    
    def valid_take(self,
                   board, 
                   pos:tuple) -> bool:
        
        if not board.in_board(pos):
            return False
        x = board.coords(pos)

        if x.contains_piece:
            if not self.same_color(x.piece.color):
                return True
        
        return False
    
class Pawn(Piece):
    def __init__(self, board, color:str, pos:tuple):
        super().__init__(board, color, pos, 'p')
        
        self.yvector = 1 if self.color == 'w' else -1
        self.double_moved = False
        self.en_passant_move = None

    def check_for_en_passant(self, board: Board):
        for x in (-1, 1):
            coords = self.pos
            coords = (coords[0] + x, coords[1])
            if board.in_board((coords)):
                square = board.coords(coords)
                if square.contains_piece:
                    if type(square.piece) is Pawn:
                        if square.piece.double_moved and board.previous_piece_to_move == square.piece:
                            self.en_passant_move = (coords[0], coords[1] + self.yvector)
                            return [self.en_passant_move]
        self.en_passant_move = None
        return []

    def get_moves(self, board) -> set:
        
        moves = []
        
        new_pos = (self.pos[0], self.pos[1] + self.yvector)


        if not board.pos_contains_piece(new_pos):
            moves.append(new_pos)
            if not self.has_moved:
                new_pos = (new_pos[0], new_pos[1] + self.yvector)
                if not board.pos_contains_piece(new_pos):

                    moves.append(new_pos)


        for x in (-1, 1):
            new_pos = add_coords(self.pos, (x, self.yvector))
            if self.valid_take(board, new_pos):
                moves.append(new_pos)

        moves += self.check_for_en_passant(board)


        return set(moves)
    
    def get_possible_attack_moves(self, board) -> set:
        moves = []
        for x in (-1, 1):
            new_pos = add_coords(self.pos, (x, self.yvector))
            if self.valid_move(board, new_pos):
                moves.append(new_pos)
        return set(moves)

class Knight(Piece):
    def __init__(self, board, color:str, pos:tuple):
        super().__init__(board, color, pos, 'kn')
        


    
    def get_moves(self, board) -> set:
        moves = []

        for vector in KNIGHT_VECTORS:
            new_coord = add_coords(self.pos, vector)
            if self.valid_move(board, new_coord):
                moves.append(new_coord)

        return set(moves)
        
    def get_possible_attack_moves(self, board) -> set:
        return self.get_moves(board)
        
class Rook(Piece):
    def __init__(self, board, color:str, pos:tuple):
        super().__init__(board, color, pos, 'r')


    def get_moves(self, board) -> set:
        moves = []
        for vector in ROOK_VECTORS:
            
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(board, pos):
                    moves.append(pos)
                
                else:
                    break

                if board.coords(pos).contains_piece:
                    break

        return set(moves)
    
    def get_possible_attack_moves(self, board) -> set:
        return self.get_moves(board)

class Bishop(Piece):
    def __init__(self, board, color:str, pos:tuple):
        super().__init__(board, color, pos, 'b')

    def get_moves(self, board) -> set:
        moves = []
        for vector in BISHOP_VECTORS:
            
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(board, pos):
                    moves.append(pos)
                else:
                    break

                if board.coords(pos).contains_piece:
                    break

        return set(moves)
        
    def get_possible_attack_moves(self, board) -> set:
        return self.get_moves(board)

class Queen(Piece):
    def __init__(self, board, color:str, pos:tuple):
        super().__init__(board, color, pos, 'q')

    def get_moves(self, board) -> set:
        moves = []
        for vector in QUEEN_VECTORS:
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(board, pos):
                    moves.append(pos)
                else:
                    break

                if board.coords(pos).contains_piece:
                    break

        return set(moves)
    
    def get_possible_attack_moves(self, board) -> set:
        return self.get_moves(board)

class King(Piece):
    def __init__(self, board, color: str, pos: tuple):
        super().__init__(board, color, pos, 'k')
        board.king_pos[color] = pos

    def move(self,
             new_board: Board,
             new_pos: tuple,
             is_simulated=False,
             is_computer=False):

        # new_board.previous_move = (self.pos, new_pos)
        # new_board.previous_piece_to_move = self

        previous_move = Move(self.pos, new_pos, board=new_board)

        new_board.coords(self.pos).update_piece(None)
        
        target_square = new_board.coords(new_pos)

        if not self.has_moved:
            match new_pos[0]:
                case 3:
                    y = new_pos[1]
                    square = new_board.coords((1, y))
                    rook = square.piece
                    
                    rook.move(new_board, (4, y), True, False)
                    


                case 7:
                    y = new_pos[1]
                    square = new_board.coords((8, y))
                    rook = square.piece
                    
                    rook.move(new_board, (6, y), True, False)
                    


        if target_square.contains_piece:
            
            
            target_square.piece.die(new_board)
            target_square.update_piece(self)
        else:
            target_square.update_piece(self)
        
        self.pos = new_pos
        self.has_moved = True
        new_board.change_current_turn()
        new_board.king_pos[self.color] = new_pos

        in_check = king_in_check(new_board)
        if not is_simulated:
            cm = can_move(new_board)


            if not cm:

                if in_check:
                    board.win_state = other_team(new_board.current_turn)
                    previous_move.flag = 'WIN'

                else:
                    board.win_state = 'd'
                    previous_move.flag = 'DRAW'

        new_board.stack.push(previous_move.to_int())
        return new_board

    def get_moves(self, board:Board) -> set:
        
        moves = []
        for vector in KING_VECTORS:
            pos = self.pos
            pos = add_coords(pos, vector)
            if self.valid_move(board, pos):
                moves.append(pos)

        if not self.has_moved:


            match self.color:
                case 'w':
                    pieces = board.white_pieces
                case 'b':
                    pieces = board.black_pieces

           
            for piece in pieces:
                if type(piece) == Rook:
                    
                    if not piece.has_moved:
                        match piece.pos[0]:
                            case 1:
                                if not (board.coords((2, piece.pos[1])).contains_piece or board.coords((3, piece.pos[1])).contains_piece or board.coords((4, piece.pos[1])).contains_piece):
                                    if self.valid_move(board, (3, piece.pos[1])):
                                        moves.append((3, piece.pos[1]))
                            case 8:

                                if not (board.coords((6, piece.pos[1])).contains_piece or board.coords((7, piece.pos[1])).contains_piece):
                                    if self.valid_move(board, (7, piece.pos[1])):
                                        moves.append((7, piece.pos[1]))
                            case _:
                                raise Exception('Could not find rook')



        return set(moves)
    
    def get_possible_attack_moves(self, board) -> set:
        return self.get_moves(board)



def init_board(board: Board):



    board.data = []
    [board.data.append(Square(WHITE_WOOD if (i % 8 + i // 8) % 2 == 1 else BLACK_WOOD)) for i in range(64)]
    board.current_turn = 'w'
    board.white_checked = False
    board.black_checked = False
    board.win_state = ''
    board.white_pieces = []
    board.black_pieces = []
    board.taken_white_pieces = []
    board.taken_black_pieces = []
    board.king_pos = {}

    for x in range(1,9):
        Pawn(board, 'w', (x, 2))
        Pawn(board, 'b', (x, 7))

    Rook(board, 'w', (1,1))
    Rook(board, 'w', (8, 1))
    Rook(board, 'b', (1, 8))
    Rook(board, 'b', (8, 8))

    Knight(board, 'w', (2, 1))
    Knight(board, 'w', (7, 1))
    Knight(board, 'b', (2, 8))
    Knight(board, 'b', (7, 8))

    Bishop(board, 'w', (3, 1))
    Bishop(board, 'w', (6, 1))
    Bishop(board, 'b', (3, 8))
    Bishop(board, 'b', (6, 8))

    King(board, 'w', (5, 1))
    Queen(board, 'w', (4, 1))

    King(board, 'b', (5, 8))
    Queen(board, 'b', (4, 8))
    
board = Board()
init_board(board)


if __name__ == '__main__':
    x = Move((8, 9), (2, 2))
    num = x.to_int()
    print (Move.from_int(num))
    