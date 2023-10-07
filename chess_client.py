import socket


def move_to_bytes(move: tuple[tuple[int, int], tuple[int, int]]) -> bytes:
    #move has two tuples with x and y from 1 to 8
    move_num = (move[0][0] - 1)
    move_num += (move[0][1] - 1) * (2 ** 3)
    move_num += (move[1][0] - 1) * (2 ** 6)
    move_num += (move[1][1] - 1) * (2 ** 9)
    return move_num.to_bytes(2)

def bytes_to_move(_bytes) -> tuple[tuple[int, int], tuple[int, int]]:
    move_num = int.from_bytes(_bytes)
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
    
    def __init__(self, server:str, port:int):
        
        self.server = server
        self.port = port

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.server, self.port))


    def send_move(self, move: tuple[tuple[int, int], tuple[int, int]]):
        self.send(move_to_bytes(move))



    def recieve_move(self):
        
        return bytes_to_move(self.recv(2))
            


    def disconnect(self):
        
        self.send_data(self.disconnect_message)

        





# conn = Connection('192.168.56.1', 5050)
# conn.send_data('beans')
# print (conn.recieve_data())
# conn.disconnect()

