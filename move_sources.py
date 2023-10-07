from chess_engine import Board
from minimax import minimax


class Move_Source:
    
    def __init__(self, team):
        self.team = team

    def get_move(self, board: Board) -> tuple:
        pass


class Minimax(Move_Source):

    def __init__(self, team: str, depth: int):
        super().__init__(team)
        self.depth = depth

    def get_move(self, board: Board) -> tuple:
        return minimax(board, self.depth)
