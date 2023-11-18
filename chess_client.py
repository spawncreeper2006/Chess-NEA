import socket

#NETWORKING
PORT = 5050
FORMAT = 'utf-8'
HEADER = 8

#SERVER_IP = '192.168.1.134'
#SERVER_IP = '192.168.56.1'
    
#for testing:
SERVER_IP = socket.gethostbyname(socket.gethostname())

def move_to_bytes(move: tuple[tuple[int, int], tuple[int, int]], flag: str = '') -> bytes:
    flag_dict = {'': 0,
                 'WIN': 1,
                 'DRAW': 2,
                 'TIMEOUT': 3,
                 'KNIGHT': 4,
                 'BISHOP': 5,
                 'ROOK': 6,
                 'QUEEN': 7}
    #move has two tuples with x and y from 1 to 8
    move_num = (move[0][0] - 1)
    move_num += (move[0][1] - 1) * (2 ** 3)
    move_num += (move[1][0] - 1) * (2 ** 6)
    move_num += (move[1][1] - 1) * (2 ** 9)
    move_num += flag_dict[flag] * (2 ** 12)

    return move_num.to_bytes(2, 'little')

def bytes_to_move(_bytes: bytes) -> tuple[tuple[tuple[int, int], tuple[int, int]], str]:

    flag_dict = {0: '',
                1: 'WIN',
                2: 'DRAW',
                3: 'TIMEOUT',
                4: 'KNIGHT',
                5: 'BISHOP',
                6: 'ROOK',
                7: 'QUEEN'}

    move_num = int.from_bytes(_bytes, 'little')
    move = [[0, 0], [0, 0]]

    move_num, move[0][0] = divmod(move_num, 8)
    move_num, move[0][1] = divmod(move_num, 8)
    move_num, move[1][0] = divmod(move_num, 8)
    move_num, move[1][1] = divmod(move_num, 8)
    flag = move_num
    print (flag)

    move[0][0] += 1
    move[0][1] += 1
    move[1][0] += 1
    move[1][1] += 1

    return (move[0][0], move[0][1]), (move[1][0], move[1][1]), flag_dict[flag]
    

class Connection(socket.socket):
    
    def __init__(self, server=SERVER_IP, port=PORT):
        
        self.server = server
        self.port = port

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.server, self.port))

    def send_bytes(self, data: bytes):
        self.send(data)


    def recieve_bytes(self, length: int) -> bytes:
        data = self.recv(length)
        while not data:
            self.recv(length)
        return data


    def send_int(self, data: int):
        self.send_bytes(data.to_bytes(1, 'little'))

    def recieve_int(self, length = 1) -> int:
        return int.from_bytes(self.recieve_bytes(length), 'little')
    
    
    def send_str(self, data: str):
        message = data.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.send_bytes(send_length)
        self.send_bytes(message)

    def recieve_str(self):

        msg_length = self.recieve_bytes(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        return self.recieve_bytes(msg_length).decode(FORMAT)

    def send_move(self, start: tuple[int, int], dest: tuple[int, int], board_state: str):

        self.send(move_to_bytes((start, dest), board_state))


    def recieve_move(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return bytes_to_move(self.recieve_bytes(2))


def establish_quickplay_connection() -> tuple[Connection, str]:
    conn = Connection()
    conn.send_int(1)
    conn.recieve_int()
    team_num = conn.recieve_int()
    match team_num:
        case 0:
            team = 'w'
        case 1:
            team = 'b'

    return conn, team

def establish_tournament_connection() -> Connection:
    conn = Connection()
    conn.send_int(2)
    return conn

if __name__ == '__main__':


    b = move_to_bytes(((1, 2), (3, 4)), 'bean')
    
    # print (b)
    print (bytes_to_move(b))

    # print (bytes_to_move(move_to_bytes(((1, 2), (3, 4)), 'd')))
    