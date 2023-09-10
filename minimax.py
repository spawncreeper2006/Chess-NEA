from chess_engine import *
from copy import deepcopy
import time
import random

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

# def minimax(board: Board, depth: int, maximising_player: bool) -> Move:

#     board = deepcopy(board)

#     if depth == 0:
#         return static_eval(board)
    
#     if maximising_player:
#         max_value = -10_000
#         for piece, pos in get_team_moves('w', board):
#             move = Move(piece, pos)
#             possible_board = piece.move(board, pos)
#             move.set_value(minimax(possible_board, depth - 1, False))
#             max_value = max(max_value, move)
#         return max_value
        
#     else:
#         min_value = 10_000
#         for piece, pos in get_team_moves('b', board):
#             move = Move(piece, pos)
#             possible_board = piece.move(board, pos)
#             move.set_value(minimax(possible_board, depth - 1, True))
#             min_value = min(min_value, move)
#         return min_value

def sim_move(board: Board,
             start: tuple[int, int],
             end: tuple[int,int]) -> Board:
    board = deepcopy(board)
    board.coords(start).piece.move(board, end)
    return board

def get_team_move_coords(team: str,
                         board:Board):
    for piece, pos in get_team_moves(team, board):
        yield piece.pos, pos

def minimax_numeric(board: Board,
             depth: int,
             max_player: bool) -> int:
    
    lambda_minimax = lambda b: minimax_numeric(b, depth - 1, not max_player)

    if depth == 0:
        return static_eval(board)
    
    if max_player:
        team = 'w'
        func = max
    else:
        team = 'b'
        func = min

    return func(map(lambda_minimax, [sim_move(board, start, end) for start, end in get_team_move_coords(team, board)]))

def minimax(board: Board,
            depth: int) -> tuple[Piece, tuple]:
    
    moves = []
    
    if board.current_turn == 'w': #maximising player
        threshold = -10_000
        for start, end in get_team_move_coords(board.current_turn, board):
            fake_board = sim_move(board, start, end)
            move_score = minimax_numeric(fake_board, depth - 1, False)
            if move_score > threshold:
                threshold = move_score
                moves = [(start, end)]

            elif move_score == threshold:
                moves.append((start, end))

    elif board.current_turn == 'b': #minimising player
        threshold = 10_000
        for start, end in get_team_move_coords(board.current_turn, board):
            fake_board = sim_move(board, start, end)
            move_score = minimax_numeric(fake_board, depth - 1, True)
            if move_score < threshold:
                threshold = move_score
                moves = [(start, end)]

            elif move_score == threshold:
                moves.append((start, end))

    if len(moves) == 1:
        move = moves[0]
        
    elif len(moves) > 1:
        move = random.choice(moves)

    else:
        raise Exception('could not find minimax move (very cursed)')

    return board.coords(move[0]).piece, move[1]

# start = time.perf_counter()

# print (minimax_numeric(board, 2, True))

# end = time.perf_counter()

# print (end-start)

# print (minimax(board, 1))