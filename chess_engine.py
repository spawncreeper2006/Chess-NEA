

KNIGHT_VECTORS = [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1), (1, 2), (-1, 2)]
ROOK_VECTORS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
BISHOP_VECTORS = [(1, 1), (-1,-1), (-1, 1), (1, -1)]
QUEEN_VECTORS = ROOK_VECTORS + BISHOP_VECTORS
KING_VECTORS = QUEEN_VECTORS

BLACK_WOOD = (145, 60, 26)
WHITE_WOOD = ( 245, 219, 135)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

white_pieces = []
black_pieces = []

def get_team_attack_moves(team:str) -> set:
    moves = []
    team_pieces = []
    match team:
        case 'w':
            team_pieces = white_pieces
        case 'b':
            team_pieces = black_pieces

    for piece in team_pieces:
        if type(piece) is Pawn:
            moves += piece.get_possible_attack_moves()
        else:
            moves += piece.get_moves()

    return set(moves)


def add_coords(c1:tuple,
               c2:tuple) -> tuple:
    if len(c1) != len(c2):
        raise Exception(f'Unable to add tuples with length {len(c1)} and length {len(c2)}')
    
    return tuple([a + b for a , b in zip(c1, c2)])

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
            print (self.piece.piece_identifier + ' Was Clicked')
            self.color = GREEN
        else:
            print ('empty square was clicked')

    def is_possible_move(self):
        self.color = BLUE

    def back_to_default_color(self):
        self.color = self.default_color

    def __str__(self):

        if self.contains_piece:
            return str(self.piece)
        else:
            return ' ' * 4

class Grid:
    def __init__(self):
        self.data = []
        [self.data.append(Square(WHITE_WOOD if (i%8 + i // 8) % 2 == 1 else BLACK_WOOD)) for i in range(64)]
        self.current_turn = 'w'

    def change_current_turn(self):
        match self.current_turn:
            case 'w':
                self.current_turn = 'b'
            case 'b':
                self.current_turn = 'w'

    def __translate_position(self, pos:tuple) -> tuple:
        pos = (pos[0]-1, pos[1]-1)
        return pos[0]+pos[1]*8

    def in_grid(self,
                pos:tuple) -> bool:
        
        for xy in pos:
            if xy < 1 or xy > 8:
                return False
        
        return True
    
    def coords(self, 
               pos:tuple) -> Square:
        
        return self.data[self.__translate_position(pos)]
    
    def pos_contains_piece(self,
                           pos:tuple) -> bool:
        return self.coords(pos).contains_piece
    

    
    def __str__(self):
        ls = [[], [], [], [], [] ,[] ,[] ,[]]

        for count, piece in enumerate(self.data):
            ls[7-count//8].append(str(piece))
        return '\n'.join([''.join(i) for i in ls])

grid = Grid()
class Piece:
    def __init__(self, color:str, pos:tuple, piece_type:str):

        self.color = color
        self.pos = pos
        grid.coords(pos).update_piece(self)
        self.has_moved = False

        if len(piece_type) == 1:
            piece_type = piece_type.upper()
        else:
            piece_type = piece_type[0].upper() + piece_type[1:]
            
        self.piece_identifier = self.color.upper() + piece_type
        self.piece_identifier = self.piece_identifier.zfill(4).replace('0', ' ')

        self.pieces = []

        match color:
            case 'w':
                white_pieces.append(self)
                self.pieces = white_pieces
            case 'b':
                black_pieces.append(self)
                self.pieces = black_pieces
        



    def die(self):
        print (f'{self} died')
        self.pieces.remove(self)


    def move(self,
             new_pos:tuple):
        grid.coords(self.pos).update_piece(None)
        target_square = grid.coords(new_pos)

        if target_square.contains_piece:
            print ('attempting to kill piece')
            
            target_square.piece.die()
            target_square.update_piece(self)
        else:
            target_square.update_piece(self)
        self.pos = new_pos
        self.has_moved = True
        grid.change_current_turn()

    def same_color(self,
                   color:str) -> bool:
        return self.color==color

    def __str__(self):
        return self.piece_identifier
    
    def valid_move(self,
                   pos:tuple) -> bool:
        if not grid.in_grid(pos):
            return False
        
        x = grid.coords(pos)

        if x.contains_piece:
            if self.same_color(x.piece.color):
                return False

        return True
    
    def valid_take(self,
                   pos:tuple) -> bool:
        
        if not grid.in_grid(pos):
            return False
        x = grid.coords(pos)

        if x.contains_piece:
            if not self.same_color(x.piece.color):
                return True
        
        return False

class Pawn(Piece):
    def __init__(self, color:str, pos:tuple):
        super().__init__(color, pos, 'p')
        
        self.yvector = 1 if self.color == 'w' else -1

    def get_moves(self) -> list:
        
        moves = []
        
        new_pos = (self.pos[0], self.pos[1] + self.yvector)


        if not grid.pos_contains_piece(new_pos):
            moves.append(new_pos)
            if not self.has_moved:
                new_pos = (new_pos[0], new_pos[1] + self.yvector)
                if not grid.pos_contains_piece(new_pos):
                    moves.append(new_pos)


        for x in (-1, 1):
            new_pos = add_coords(self.pos, (x, self.yvector))
            if self.valid_take(new_pos):
                moves.append(new_pos)

        return moves
    
    def get_possible_attack_moves(self) -> list:
        moves = []
        for x in (-1, 1):
            new_pos = add_coords(self.pos, (x, self.yvector))
            if self.valid_move(new_pos):
                moves.append(new_pos)
        return moves

class Knight(Piece):
    def __init__(self, color:str, pos:tuple):
        super().__init__(color, pos, 'kn')


    
    def get_moves(self):
        moves = []

        for vector in KNIGHT_VECTORS:
            new_coord = add_coords(self.pos, vector)
            if self.valid_move(new_coord):
                moves.append(new_coord)

        return moves
        
class Rook(Piece):
    def __init__(self, color:str, pos:tuple):
        super().__init__(color, pos, 'r')


    def get_moves(self):
        moves = []
        for vector in ROOK_VECTORS:
            
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(pos):
                    moves.append(pos)
                
                else:
                    break

                if grid.coords(pos).contains_piece:
                    break

        return moves

class Bishop(Piece):
    def __init__(self, color:str, pos:tuple):
        super().__init__(color, pos, 'b')

    def get_moves(self):
        moves = []
        for vector in BISHOP_VECTORS:
            
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(pos):
                    moves.append(pos)
                else:
                    break

                if grid.coords(pos).contains_piece:
                    break

        return moves

class Queen(Piece):
    def __init__(self, color:str, pos:tuple):
        super().__init__(color, pos, 'q')

    def get_moves(self):
        moves = []
        for vector in QUEEN_VECTORS:
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(pos):
                    moves.append(pos)
                else:
                    break

                if grid.coords(pos).contains_piece:
                    break

        return moves

class King(Piece):
    def __init__(self, color:str, pos:tuple):
        super().__init__(color, pos, 'k')

    def get_moves(self):
        moves = []
        for vector in KING_VECTORS:
            pos = self.pos
            pos = add_coords(pos, vector)
            if self.valid_move(pos):
                moves.append(pos)


        return moves



def init_board():

    for x in range(1,9):
        Pawn('w', (x, 2))
        Pawn('b', (x, 7))

    Rook('w', (1,1))
    Rook('w', (8, 1))
    Rook('b', (1, 8))
    Rook('b', (8, 8))

    Knight('w', (2, 1))
    Knight('w', (7, 1))
    Knight('b', (2, 8))
    Knight('b', (7, 8))

    Bishop('w', (3, 1))
    Bishop('w', (6, 1))
    Bishop('b', (3, 8))
    Bishop('b', (6, 8))

    King('w', (5, 1))
    Queen('w', (4, 1))

    King('b', (5, 8))
    Queen('b', (4, 8))




init_board()

# #x = Rook('w', (4, 1))
# #y = Pawn('w', (5, 1))



# #print (y.get_possible_attack_moves())
# print (grid.coords((1, 2)).piece.get_moves())
# grid.coords((1, 2)).piece.move((1, 3))
# print (grid.coords((1,3)).piece.get_moves())
