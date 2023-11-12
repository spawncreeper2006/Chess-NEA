import socket
import threading
from circular_queue import Circular_Queue
from client import Client
from network_constants import ADDR, SERVER


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
        print (clients)
        self.play_match(clients[0], clients[1])


class Tournament(Gamemode):
    
    def __init__(self):
        super().__init__(4)





class Client_Queue:
    def __init__(self, gamemode: Gamemode):
        self.gamemode = gamemode
        self.required_clients = gamemode.required_clients
        self.queue = Circular_Queue(self.required_clients)

    def new_connection(self, client: Client):

        self.queue.enqueue(client)
        if self.queue.is_full():
            print (self.queue)
            self.gamemode.start(self.queue.dequeue_all())

        print ('new client', client)




queues = {1: Client_Queue(Quickplay()),
          2: Client_Queue(Tournament())}


def handle_client(conn: socket.socket, addr: str):
    client = Client(conn, addr)

    print (f'GAMEMODE {client.gamemode}')
    queues[client.gamemode].new_connection(client)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == '__main__':
    main()
