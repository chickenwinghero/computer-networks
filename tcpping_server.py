# tcpping_server.py
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print('Connection from', addr[0])
    buffer = ''
    while True:
        data = connectionSocket.recv(1024)
        if data == b'':
            break
        buffer += data.decode()
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            print('From', addr[0], ':', line)
            connectionSocket.send((line.upper() + '\n').encode())
    connectionSocket.close()
    print('Connection closed')
