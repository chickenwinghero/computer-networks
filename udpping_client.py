# udpping_client.py
import sys
import time
from socket import *

serverName = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
numProbes = int(sys.argv[2]) if len(sys.argv) > 2 else 10
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)

rtts = []

for seq in range(1, numProbes + 1):
    sendTime = time.time()
    message = f'ping {seq} {sendTime:.6f}'
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    try:
        reply, serverAddress = clientSocket.recvfrom(2048)
        rtt = (time.time() - sendTime) * 1000.0
        rtts.append(rtt)
        print(f'{seq:2d}  {reply.decode()}      rtt {rtt:8.3f} ms')
    except timeout:
        print(f'{seq:2d}  request timed out')

clientSocket.close()

received = len(rtts)
lost = numProbes - received
lossPct = (lost / numProbes * 100.0) if numProbes > 0 else 0.0

print()
print(f'--- {serverName} udp ping statistics ---')
print(f'{numProbes} probes sent, {received} replies, {lost} lost, {lossPct:.1f}% loss')
if rtts:
    print(f'rtt min/avg/max = {min(rtts):.3f}/{sum(rtts) / len(rtts):.3f}/{max(rtts):.3f} ms')
else:
    print('rtt min/avg/max = n/a (no replies)')
