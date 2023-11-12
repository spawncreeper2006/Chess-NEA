import socket

#NETWORKING
PORT = 5050
FORMAT = 'utf-8'
HEADER = 8

#SERVER_IP = '192.168.1.134'
SERVER_IP = '192.168.56.1'


def move_to_bytes(move: tuple[tuple[int, int], tuple[int, int]], board_state: str) -> bytes:
    #move has two tuples with x and y from 1 to 8
    move_num = (move[0][0] - 1)
    move_num += (move[0][1] - 1) * (2 ** 3)
    move_num += (move[1][0] - 1) * (2 ** 6)
    move_num += (move[1][1] - 1) * (2 ** 9)
    if board_state:
        if board_state == 'd':
            move_num += 2 ** 12
        else:
            move_num += 2 ** 13
    return move_num.to_bytes(2)

def bytes_to_move(_bytes: bytes) -> tuple[tuple[int, int], tuple[int, int]]:
    move_num = int.from_bytes(_bytes)
    move_num %= 2 ** 12
    move = [[0, 0], [0, 0]]

    move_num, move[0][0] = divmod(move_num, 8)
    move_num, move[0][1] = divmod(move_num, 8)
    move_num, move[1][0] = divmod(move_num, 8)
    move[1][1] = move_num

    move[0][0] += 1
    move[0][1] += 1
    move[1][0] += 1
    move[1][1] += 1

    return (move[0][0], move[0][1]), (move[1][0], move[1][1])
    

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

    def send_move(self, start: tuple[int, int], dest: tuple[int, int]):
        self.send(move_to_bytes(start, dest))


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


    conn = Connection('192.168.56.1', 5050)
    conn.send_int(1)

    # print (bytes_to_move(move_to_bytes(((1, 2), (3, 4)), 'd')))
    