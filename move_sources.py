from chess_engine import Board
from minimax import minimax
from chess_client import Connection

class Move_Source:
    
    def __init__(self, team: str):
        self.team = team

    def get_move(self, board: Board) -> tuple:
        pass


class Minimax(Move_Source):

    def __init__(self, team: str, depth: int):
        super().__init__(team)
        self.depth = depth

    def get_move(self, board: Board) -> tuple:
        return minimax(board, self.depth)

#ONLINE
#QUICKPLAY: 1
#TOURNEMANT: 2

teams = ['w', 'b']

class Quickplay(Move_Source):

    def __init__(self, conn: Connection):
        self.conn = conn
        super().__init__('')
    
    def get_move(self, board: Board) -> tuple:
        if not board.previous_move == ():

            start, dest = board.previous_move
            self.conn.send_move(start, dest, board.win_state)
        
        start, dest = self.conn.recieve_move()

        return (board.coords(start).piece, dest)
        
    