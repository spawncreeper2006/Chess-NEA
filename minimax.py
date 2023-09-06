from chess_engine import *
from copy import deepcopy

class Move:
    def __init__(self, piece:Piece, pos:tuple, value=None):
        self.piece = piece
        self.start_pos = piece.pos
        self.pos = pos
        self.value = value

    def set_value(self, value):
        self.value = int(value)
        

    def __int__(self):
        return self.value

    def __gt__(self, operand):
        return self.value > int(operand)
    
    def __lt__(self, operand):
        return self.value < int(operand)
    
    def __str__(self) -> str:
        return f'{type(self.piece)} @ {self.start_pos} -> {self.pos}'
    

#piece worth source: https://www.masterclass.com/articles/chess-piece-guide

piece_worth = {Pawn: 1,
               Knight: 3,
               Bishop: 3,
               Rook: 5,
               Queen: 9,
               King: 1000}


def static_eval(board: Board):
    board_worth = 0
    for white_piece in board.white_pieces:
        board_worth += piece_worth[type(white_piece)]

    for black_piece in board.black_pieces:
        board_worth -= piece_worth[type(black_piece)]

    return board_worth

def minimax(board: Board, depth: int, maximising_player: bool) -> Move:

    board = deepcopy(board)

    if depth == 0:
        return static_eval(board)
    
    if maximising_player:
        max_value = -10_000
        for piece, pos in get_team_moves('w', board):
            move = Move(piece, pos)
            possible_board = piece.move(board, pos)
            move.set_value(minimax(possible_board, depth - 1, False))
            max_value = max(max_value, move)
        return max_value
        
    else:
        min_value = 10_000
        for piece, pos in get_team_moves('b', board):
            move = Move(piece, pos)
            possible_board = piece.move(board, pos)
            move.set_value(minimax(possible_board, depth - 1, True))
            min_value = min(min_value, move)
        return min_value
