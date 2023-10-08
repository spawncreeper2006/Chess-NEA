import socket
import threading
from circular_queue import Circular_Queue
from client import Client
from network_constants import ADDR, SERVER
from gamemodes import Gamemode, Quickplay, Tournament



    


class Client_Queue:
    def __init__(self, gamemode: Gamemode):
        self.gamemode = gamemode
        self.required_clients = gamemode.required_clients
        self.queue = Circular_Queue(self.required_clients)

    def new_connection(self, client: Client):

        self.queue.enqueue(client)
        if self.queue.is_full():
            self.gamemode.start(self.queue.dequeue_all())




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
