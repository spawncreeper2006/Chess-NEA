from socket import gethostbyname, gethostname

FORMAT = 'utf-8'
HEADER = 8
PORT = 5050
SERVER = gethostbyname(gethostname())
ADDR = (SERVER, PORT)
