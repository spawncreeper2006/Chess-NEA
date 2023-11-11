from chess_engine import *
from copy import deepcopy
import time
import random


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


def sim_move(board: Board,
             start: tuple[int, int],
             end: tuple[int,int]) -> Board:
    board = deepcopy(board)
    board.coords(start).piece.move(board, end, is_simulated=True)
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

def minimax_numeric_ab(board: Board,
                       depth: int,
                       max_player: bool,
                       alpha: int,
                       beta: int) -> int:
    

    if depth == 0:
        return static_eval(board)
    
    if max_player:
        score = -10000
        for start, end in get_team_move_coords('w', board):
            
            score = max(score, minimax_numeric_ab(sim_move(board, start, end), depth - 1, False, alpha, beta))
            alpha = max(alpha, score)

            if beta <= alpha:
                print ('pruned')
                break

    else:
        score = 10000
        for start, end in get_team_move_coords('b', board):
            
            score = min(score, minimax_numeric_ab(sim_move(board, start, end), depth - 1, True, alpha, beta))
            beta = min(beta, score)

            if beta <= alpha:
                print ('pruned')
                break


    return score

def minimax(board: Board,
            depth: int) -> tuple[Piece, tuple]:
    
    moves = []
    
    if board.current_turn == 'w': #maximising player
        threshold = -10_000
        for start, end in get_team_move_coords(board.current_turn, board):
            fake_board = sim_move(board, start, end)
            move_score = minimax_numeric_ab(fake_board, depth - 1, False, -10_000, 10_000)
            if move_score > threshold:
                threshold = move_score
                moves = [(start, end)]

            elif move_score == threshold:
                moves.append((start, end))

    elif board.current_turn == 'b': #minimising player
        threshold = 10_000
        for start, end in get_team_move_coords(board.current_turn, board):
            fake_board = sim_move(board, start, end)
            move_score = minimax_numeric_ab(fake_board, depth - 1, True, -10_000, 10_000)
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

