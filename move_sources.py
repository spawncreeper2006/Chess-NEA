from chess_engine import Board
from minimax import minimax
from chess_client import Connection

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

#ONLINE
#QUICKPLAY: 1
#TOURNEMANT: 2

teams = ['w', 'b']

class Quickplay(Move_Source):

    def __init__(self):
        self.conn = Connection()
        self.conn.send_int(1)
        self.conn.recieve_int() #waits for other player
        team = teams[self.conn.recieve_int()]
        super().__init__(team)
    
    def get_move(self, board: Board) -> tuple:
        self.conn.send_move(board)
        return self.conn.recieve_move()
    
    