
from copy import deepcopy, copy

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




def in_grid(pos:tuple) -> bool:
    for xy in pos:
        if xy < 1 or xy > 8:
            return False

    return True

def get_team_moves(team:str, this_grid):
    moves = []
    team_pieces = []
    match team:
        case 'w':
            team_pieces = this_grid.white_pieces
        case 'b':
            team_pieces = this_grid.black_pieces

    for piece in team_pieces:
        moves = piece.get_moves(this_grid)
        for move in moves:
            yield (piece, move)

def get_team_attack_moves(team:str, this_grid) -> set:
    
    moves = []
    team_pieces = []
    match team:
        case 'w':
            team_pieces = this_grid.white_pieces
        case 'b':
            team_pieces = this_grid.black_pieces

    for piece in team_pieces:

        moves += piece.get_possible_attack_moves(this_grid)


    return set(moves)

def does_not_endanger_king(piece, grid, pos) -> bool:
    possible_grid = deepcopy(grid)
    
    piece_position = piece.pos
    piece = possible_grid.coords(piece_position).piece
    possible_grid = piece.move(possible_grid, pos)
    
    enemy_attack_moves = get_team_attack_moves(possible_grid.current_turn, possible_grid)
    
    return not possible_grid.king_pos[other_team(possible_grid.current_turn)] in enemy_attack_moves
        


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
        
def king_in_check(grid):
    if grid.king_pos[grid.current_turn] in get_team_attack_moves(other_team(grid.current_turn), grid):
        match grid.current_turn:
            case 'w':
                grid.white_checked = True
                
            case 'b':
                grid.black_checked = True

        return True

    else:
        grid.white_checked = False
        grid.black_checked = False

    return False

def can_move(grid):
    for (piece, move) in get_team_moves(grid.current_turn, grid):
        if does_not_endanger_king(piece, grid, move):
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

class Grid:
    def __init__(self):
        self.data = []
        [self.data.append(Square(WHITE_WOOD if (i % 8 + i // 8) % 2 == 1 else BLACK_WOOD)) for i in range(64)]
        self.current_turn = 'w'
        self.white_checked = False
        self.black_checked = False
        self.win_state = ''
        self.white_pieces = []
        self.black_pieces = []
        self.taken_white_pieces = []
        self.taken_black_pieces = []
        self.king_pos = {}


    def change_current_turn(self):
        match self.current_turn:
            case 'w':
                self.current_turn = 'b'
            case 'b':
                self.current_turn = 'w'

    def translate_position(self, pos:tuple) -> tuple:
        pos = (pos[0]-1, pos[1]-1)
        return pos[0]+pos[1]*8

    def in_grid(self,
                pos:tuple) -> bool:
        return in_grid(pos)

    
    def coords(self, 
               pos:tuple) -> Square:
        
        return self.data[self.translate_position(pos)]
    
    def pos_contains_piece(self,
                           pos:tuple) -> bool:
        return self.coords(pos).contains_piece
    

    
    def __str__(self):
        ls = [[], [], [], [], [] ,[] ,[] ,[]]

        for count, piece in enumerate(self.data):
            ls[7-count//8].append(str(piece))
        return '\n'.join([''.join(i) for i in ls])


class Piece:
    def __init__(self, grid, color:str, pos:tuple, piece_type:str):

        

        self.color = color
        self.pos = pos
        grid.coords(pos).update_piece(self)
        self.has_moved = False

        if len(piece_type) == 1:
            piece_type = piece_type.upper()
        else:
            piece_type = piece_type[0].upper() + piece_type[1:]
            
        self.piece_identifier = self.color.upper() + piece_type


        self.pieces = []

        match color:
            case 'w':
                grid.white_pieces.append(self)
                self.pieces = grid.white_pieces
            case 'b':
                grid.black_pieces.append(self)
                self.pieces = grid.black_pieces


        



    def die(self, new_grid:Grid):
        self.pieces.remove(self)
        pieces = []
        team = ''
        match self.color:
            case 'w':
                pieces = new_grid.taken_white_pieces
                team = 'W'
            case 'b':
                pieces = new_grid.taken_black_pieces
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
            case _:
                raise Exception('could not find piece')
        


        


    def move(self,
             new_grid:Grid,
             new_pos:tuple,
             check_for_win=False):

        new_grid.coords(self.pos).update_piece(None)
        
        target_square = new_grid.coords(new_pos)

        if target_square.contains_piece:

            
            target_square.piece.die(new_grid)
            target_square.update_piece(self)
        else:
            target_square.update_piece(self)
        
        self.pos = new_pos
        self.has_moved = True
        new_grid.change_current_turn()

        in_check = king_in_check(new_grid)
        if check_for_win:

            cm = can_move(new_grid)


            if not cm:

                if in_check:
                    grid.win_state = other_team(new_grid.current_turn)

                else:
                    grid.win_state = 'd'



        return new_grid

    def same_color(self,
                   color:str) -> bool:
        return self.color==color

    def __str__(self):
        return self.piece_identifier.zfill(4).replace('0', ' ')
    
    def valid_move(self,
                   grid,
                   pos:tuple) -> bool:
        if not grid.in_grid(pos):
            return False
        
        x = grid.coords(pos)

        if x.contains_piece:
            if self.same_color(x.piece.color):
                return False

        return True
    
    def valid_take(self,
                   grid, 
                   pos:tuple) -> bool:
        
        if not grid.in_grid(pos):
            return False
        x = grid.coords(pos)

        if x.contains_piece:
            if not self.same_color(x.piece.color):
                return True
        
        return False

class Pawn(Piece):
    def __init__(self, grid, color:str, pos:tuple):
        super().__init__(grid, color, pos, 'p')
        
        self.yvector = 1 if self.color == 'w' else -1

    def get_moves(self, grid) -> set:
        
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
            if self.valid_take(grid, new_pos):
                moves.append(new_pos)

        return set(moves)
    
    def get_possible_attack_moves(self, grid) -> set:
        moves = []
        for x in (-1, 1):
            new_pos = add_coords(self.pos, (x, self.yvector))
            if self.valid_move(grid, new_pos):
                moves.append(new_pos)
        return set(moves)

class Knight(Piece):
    def __init__(self, grid, color:str, pos:tuple):
        super().__init__(grid, color, pos, 'kn')
        


    
    def get_moves(self, grid) -> set:
        moves = []

        for vector in KNIGHT_VECTORS:
            new_coord = add_coords(self.pos, vector)
            if self.valid_move(grid, new_coord):
                moves.append(new_coord)

        return set(moves)
        
    def get_possible_attack_moves(self, grid) -> set:
        return self.get_moves(grid)
        
class Rook(Piece):
    def __init__(self, grid, color:str, pos:tuple):
        super().__init__(grid, color, pos, 'r')


    def get_moves(self, grid) -> set:
        moves = []
        for vector in ROOK_VECTORS:
            
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(grid, pos):
                    moves.append(pos)
                
                else:
                    break

                if grid.coords(pos).contains_piece:
                    break

        return set(moves)
    
    def get_possible_attack_moves(self, grid) -> set:
        return self.get_moves(grid)

class Bishop(Piece):
    def __init__(self, grid, color:str, pos:tuple):
        super().__init__(grid, color, pos, 'b')

    def get_moves(self, grid) -> set:
        moves = []
        for vector in BISHOP_VECTORS:
            
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(grid, pos):
                    moves.append(pos)
                else:
                    break

                if grid.coords(pos).contains_piece:
                    break

        return set(moves)
        
    def get_possible_attack_moves(self, grid) -> set:
        return self.get_moves(grid)

class Queen(Piece):
    def __init__(self, grid, color:str, pos:tuple):
        super().__init__(grid, color, pos, 'q')

    def get_moves(self, grid) -> set:
        moves = []
        for vector in QUEEN_VECTORS:
            pos = self.pos
            while True:
                pos = add_coords(pos, vector)
                if self.valid_move(grid, pos):
                    moves.append(pos)
                else:
                    break

                if grid.coords(pos).contains_piece:
                    break

        return set(moves)
    
    def get_possible_attack_moves(self, grid) -> set:
        return self.get_moves(grid)

class King(Piece):
    def __init__(self, grid, color:str, pos:tuple):
        super().__init__(grid, color, pos, 'k')
        grid.king_pos[color] = pos

    def move(self,
             new_grid:Grid,
             new_pos:tuple,
             check_for_win=False):

        new_grid.coords(self.pos).update_piece(None)
        
        target_square = new_grid.coords(new_pos)

        if target_square.contains_piece:
            
            
            target_square.piece.die(new_grid)
            target_square.update_piece(self)
        else:
            target_square.update_piece(self)
        
        self.pos = new_pos
        self.has_moved = True
        new_grid.change_current_turn()
        new_grid.king_pos[self.color] = new_pos

        in_check = king_in_check(new_grid)
        if check_for_win:
            cm = can_move(new_grid)


            if not cm:

                if in_check:
                    grid.win_state = other_team(new_grid.current_turn)

                else:
                    grid.win_state = 'd'
        return new_grid

    def get_moves(self, grid) -> set:
        
        moves = []
        for vector in KING_VECTORS:
            pos = self.pos
            pos = add_coords(pos, vector)
            if self.valid_move(grid, pos):
                moves.append(pos)


        return set(moves)
    
    def get_possible_attack_moves(self, grid) -> set:
        return self.get_moves(grid)



def init_board(grid):

    for x in range(1,9):
        Pawn(grid, 'w', (x, 2))
        Pawn(grid, 'b', (x, 7))

    Rook(grid, 'w', (1,1))
    Rook(grid, 'w', (8, 1))
    Rook(grid, 'b', (1, 8))
    Rook(grid, 'b', (8, 8))

    Knight(grid, 'w', (2, 1))
    Knight(grid, 'w', (7, 1))
    Knight(grid, 'b', (2, 8))
    Knight(grid, 'b', (7, 8))

    Bishop(grid, 'w', (3, 1))
    Bishop(grid, 'w', (6, 1))
    Bishop(grid, 'b', (3, 8))
    Bishop(grid, 'b', (6, 8))

    King(grid, 'w', (5, 1))
    Queen(grid, 'w', (4, 1))

    King(grid, 'b', (5, 8))
    Queen(grid, 'b', (4, 8))



grid = Grid()
init_board(grid)


