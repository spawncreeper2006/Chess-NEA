import threading
from client import Client


def check_win_state(data: bytes) -> str:

    num = int.from_bytes(data)
    if num >= 2 ** 13:
        return 'w'
    elif num >= 2 ** 12:
        return 'd'
    else:
        return ''

class Gamemode:
    def __init__(self, required_clients):
        self.required_clients = required_clients

    def start(self, clients: list[Client]):
        pass

    def play_match(self, client1: Client, client2: Client) -> str: #w, d, b
        client1.send_start_signal('w')
        client2.send_start_signal('b')
        
        while True:
            move = client1.recieve_bytes(2)

            win_state = check_win_state(move)
            client2.send_bytes(move)

            if win_state != '':
                return win_state
                
            move = client2.recieve_bytes(2)
            client1.send_bytes(move)

            if win_state != '':
                return win_state if win_state != 'w' else 'b'

    def start_thread(self, clients: list):
        threading.Thread(target = self.start, args=(clients)).start()

class Quickplay(Gamemode):

    def __init__(self):
        super().__init__(2)

    def start(self, clients: list):
        self.play_match(clients[0], clients[1])


class Tournament(Gamemode):
    
    def __init__(self):
        super().__init__(4)

