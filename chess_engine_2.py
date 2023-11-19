
import numpy as np
from move import Move
from stack import NP_Stack, Stack
from typing import Generator, Literal

#COLOR

#vectors
KNIGHT_VECTORS = np.array([(2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1), (1, 2), (-1, 2)])
ROOK_VECTORS =  np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])
BISHOP_VECTORS = np.array([(1, 1), (-1,-1), (-1, 1), (1, -1)])
QUEEN_VECTORS = np.concatenate([ROOK_VECTORS, BISHOP_VECTORS])
KING_VECTORS = QUEEN_VECTORS

#colors
BLACK_WOOD = (145, 60, 26)
WHITE_WOOD = (245, 219, 135)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Square:
    def __init__(self):
        self.piece = None

    def remove_piece(self):
        self.piece = None
    


class Piece:
    def __init__(self, piece_char: str, color: Literal['w', 'b']):
        self.piece_char = piece_char
        self.color = color
        self.piece_identifier = self.color.upper() + self.piece_char.capitalize()

    def is_enemy(self, piece):
        return self.color != piece.color
    
        
    def get_moves_from_vectors(self, pos: np.ndarray, board, vectors: np.ndarray) -> np.ndarray:
        moves = []
        for vector in vectors:
            for move in Board.follow_vector(pos, vector):
                if board.piece_in_pos(move):
                    if self.is_enemy(board[move].piece):
                        moves.append(move)

                    break
                else:
                    moves.append(move)

        return np.array(moves)

    def get_moves(self, pos, board) -> np.ndarray:
        pass

    def get_attack_moves(self, pos, board) -> np.ndarray:
        pass

    def add_move(self, moves: list, coords: np.ndarray):
        moves.append(tuple(coords))

    def __str__(self):
        return self.piece_identifier

class Board:
    def __init__(self):
        self.__data = np.array([Square() for _ in range(64)], dtype=Square)
        self.current_turn = 'w'
        self.checked = {'w': False, 'b': False}
        self.pieces = {'w': [], 'b': []}
        self.taken_pieces = {'w': [], 'b': []}
        self.king_pos = {}

        self.win_state = ''
        self.previous_piece_to_move = None

        self.stack = NP_Stack(512)
        self.taken_piece_stack = Stack(32)

    def other_color(color: str):
        return 'w' if color == 'b' else 'b'
    
    def concat_moves(moves) -> np.ndarray:
        conc_array = moves[0]
        for array in moves[1:]:
            if len(array) != 0:
                conc_array = np.concatenate([conc_array, array])



    def change_current_turn(self):
        self.current_turn = Board.other_color(self.current_turn)

    def __translate_position(self, pos: np.ndarray) -> tuple:
        pos = (pos[0] - 1, pos[1] - 1)
        return pos[0] + pos[1] * 8
    

    def __getitem__(self, coords: tuple) -> Square:
        # print (coords)
        return self.__data[self.__translate_position(coords)]
    
    def __setitem__(self, coords: tuple, value: Square):
        self.__data[self.__translate_position(coords)] = value

    def contains(array: np.ndarray) -> bool:
        for xy in array:
            if xy < 1 or xy > 8:
                return False
            
        return True
    
    def follow_vector(start: np.ndarray, vector: np.ndarray) -> Generator[np.ndarray, None, None]:
        iters = 7
        
        for sxy, vxy in zip(start, vector):
            match vxy:
                case 1:
                    iters = min(8 - sxy, iters)
                case -1:
                    iters = min(sxy - 1, iters)
                case 0:
                    pass
        pos = start
        for _ in range(iters):
            pos += vector
            yield np.array(pos)

    def find_pieces(self):
        self.pieces = {'w': [], 'b': []}
        for x, y in zip(range(1, 9), range(1, 9)):
            if self[x, y].piece != None:
                piece = self[x, y].piece
                self.pieces[piece.color].append((x, y))
    
    def piece_in_pos(self, pos):
        return self[pos].piece != None
    
    def kill_piece(self, piece: Piece):
        self.taken_pieces[piece.color].append(piece)
        self.taken_piece_stack.push(piece)

    def revive_piece(self, pos: tuple[int, int]):
        piece = self.taken_piece_stack.pop()
        self.taken_pieces[piece.color].remove(piece)
        self[pos].piece = piece

    def get_discovered_check_by_color(self, color: Literal['w', 'b']):
        moves = []
        for position in self.pieces[color]:
            piece = self[position].piece
            if piece.piece_char in ('q', 'r', 'b'):
                moves.append(piece.get_attack_moves())

        return Board.concat_moves(moves)
    
    
    def can_move(self, color: Literal['w', 'b']):
        pass

    
    def move(self, move_array: np.ndarray, flip: bool = True, human: bool = False):
        
        start_square = self[move_array[0]]
        piece = start_square.piece
        self.previous_piece_to_move = piece
        
        move = Move(move_array[0], move_array[1])
        start_square.remove_piece()

        dest_square = self[move_array[1]]
        if dest_square.piece != None:
            move.flags += ('TAKE',)
            self.kill_piece(dest_square.piece)

        self[move_array[1]].piece = piece

        match piece.piece_char:
            case 'p':
                piece.has_moved = True
            case 'k':
                self.king_pos[self.current_turn] = move_array[1]
            case _:
                pass

        self.stack.push(move.to_int())

        if flip:
            self.change_current_turn()
        

    def can_undo(self):
        return not self.stack.is_empty()
    
    def undo(self, flip: bool = True):
        
        move = Move.from_int(self.stack.pop())
        square = self[move.dest]
        piece = square.piece
        square.remove_piece()
        self[move.start].piece = piece

        if 'TAKE' in move.flags:
            self.revive_piece(move.dest)

        if piece.piece_char == 'p' and abs(move.start[1] - move.dest[1]) == 2:
            piece.has_moved = False

        self.change_current_turn()
        

    def __str__(self):
        _str = ''

        for count, item in enumerate(np.flip(self.__data)):
            
            _str += str(item.piece).ljust(5) if item.piece != None else ' ' * 5
            if count % 8 == 7:
                _str += '\n'
            
        return _str



class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__('p', color)
        self.has_moved = False
        self.yvector = np.array([0, 1]) if self.color == 'w' else np.array([0, -1])
        self.take_vectors = np.array([self.yvector + (1, 0), self.yvector + (-1, 0)])
    
    def __get_attack_moves(self, pos: np.ndarray, board: Board) -> list:
        moves = []
        for take_pos in self.take_vectors + pos:
            square = board[take_pos]
            if square.piece != None:
                if self.is_enemy(square.piece):
                    self.add_move(moves, take_pos)
                
        return moves

    def get_attack_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:

        return np.array(self.__get_attack_moves(pos, board))

    def get_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        moves = []
        move = pos + self.yvector
        if not board.piece_in_pos(move):
            self.add_move(moves, move)

            if not self.has_moved:
                move += self.yvector

                if not board.piece_in_pos(move):
                    self.add_move(moves, move)


        return np.array(moves + self.__get_attack_moves(pos, board))

        

class Knight(Piece):
    def __init__(self, color: str):
        super().__init__('kn', color)

    def get_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        moves = []
        for vector in KNIGHT_VECTORS:
            move = pos + vector
            if Board.contains(move):
                if board.piece_in_pos(move):
                    
                    if self.is_enemy(board[move].piece):
                        self.add_move(moves, move)
                else:
                    self.add_move(moves, move)

        return np.array(moves)
    
    def get_attack_moves(self, pos, board) -> np.ndarray:
        return self.get_moves(pos, board)

class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__('b', color)

    def get_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        return self.get_moves_from_vectors(pos, board, BISHOP_VECTORS)
    
    def get_attack_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        return self.get_moves(pos, board)

class Rook(Piece):
    def __init__(self, color: str):
        super().__init__('r', color)

    def get_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        
        return self.get_moves_from_vectors(pos, board, ROOK_VECTORS)
    
    def get_attack_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        return self.get_moves(pos, board)

class Queen(Piece):
    def __init__(self, color: str):
        super().__init__('q', color)

    def get_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        return self.get_moves_from_vectors(pos, board, QUEEN_VECTORS)
    
    def get_attack_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        return self.get_moves(pos, board)


class King(Piece):
    def __init__(self, color: str):
        super().__init__('k', color)

    def get_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        moves = []
        for move in KING_VECTORS + pos:
            if Board.contains(move):
                square = board[move]
                if square.piece != None:
                    if self.is_enemy(square.piece):
                        self.add_move(moves, move)
                else:
                    self.add_move(moves, move)
        
        return np.array(moves)
            
    
    def get_attack_moves(self, pos: np.ndarray, board: Board) -> np.ndarray:
        return self.get_moves(pos, board)


def create_board() -> Board:
    
    board = Board()
    
    for x in range(1, 9):
        board[x, 2].piece = Pawn('w')
        board[x, 7].piece = Pawn('b')

    for color, y in (('w', 1), ('b', 8)):
        board[1, y].piece = Rook(color)
        board[2, y].piece = Knight(color)
        board[3, y].piece = Bishop(color)
        board[4, y].piece = Queen(color)
        board[5, y].piece = King(color)
        board[6, y].piece = Bishop(color)
        board[7, y].piece = Knight(color)
        board[8, y].piece = Rook(color)

    board.find_pieces()

    return board




# if __name__ == '__main__':
#     b = create_board()
#     # king = b[5, 1].piece
#     # print (king.get_moves(np.array((5, 1)), b))

#     print (b.pieces['w'][0])
#     # start_pos = np.array([3, 1])
#     # vector = np.array([-1, 1])
#     # print (list(Board.follow_vector(start_pos, vector)))
