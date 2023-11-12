
from socket import socket
from network_constants import FORMAT, HEADER




class Client:
    def __init__(self, connection: socket, ip_addr: str):
        
        self.connection = connection
        self.ip_addr = ip_addr
        self.gamemode = self.recieve_int()

    def send_bytes(self, data: bytes):
        self.connection.send(data)


    def recieve_bytes(self, length: int) -> bytes:
        data = self.connection.recv(length)
        print (data)
        while not data:
            self.connection.recv(length)
        return data


    def send_int(self, data: int):
        self.send_bytes(data.to_bytes(1))

    def recieve_int(self, length=1) -> int:
        return int.from_bytes(self.recieve_bytes(length))
    
    
    def send_str(self, data: str):
        message = data.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.send_bytes(send_length)
        self.send_bytes(message)

    def recieve_str(self) -> str:

        msg_length = self.recieve_bytes(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        return self.recieve_bytes(msg_length).decode(FORMAT)
    
    def send_lobby_size(self, lobby_size: int):
        self.send_int(lobby_size)

    def send_start_signal(self, team: str):
        self.send_int(255)
        match team:
            case 'w':
                self.send_int(0)
            case 'b':
                self.send_int(1)

