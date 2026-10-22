# udpping_server.py
from socket import *
import random
lossRate = 0.2
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('From', clientAddress[0], ':', message.decode())
    if random.random() < lossRate:
        print('You lost the gamble')
    else:
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
