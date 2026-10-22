# tcpping_client.py
import sys
import time
from socket import *

serverName = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
numProbes = int(sys.argv[2]) if len(sys.argv) > 2 else 10
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(1.0)

connectStart = time.time()
try:
    clientSocket.connect((serverName, serverPort))
except (timeout, OSError) as e:
    print(f'could not connect to {serverName}:{serverPort} ({e})')
    sys.exit(1)
handshakeMs = (time.time() - connectStart) * 1000.0
print(f'TCP handshake (connect)      {handshakeMs:8.3f} ms')
print()

rtts = []
timeouts = 0
buffer = ''
closed = False

for seq in range(1, numProbes + 1):
    sendTime = time.time()
    message = f'ping {seq} {sendTime:.6f}\n'
    clientSocket.send(message.encode())
    try:
        while '\n' not in buffer:
            data = clientSocket.recv(1024)
            if data == b'':
                closed = True
                break
            buffer += data.decode()
        if closed:
            print(f'{seq:2d}  connection closed by server')
            break
        rtt = (time.time() - sendTime) * 1000.0
        reply, buffer = buffer.split('\n', 1)
        rtts.append(rtt)
        print(f'{seq:2d}  {reply}      rtt {rtt:8.3f} ms')
    except timeout:
        timeouts += 1
        print(f'{seq:2d}  request timed out')

clientSocket.close()

received = len(rtts)
lost = numProbes - received
lossPct = (lost / numProbes * 100.0) if numProbes > 0 else 0.0

print()
print(f'--- {serverName} tcp ping statistics ---')
print(f'{numProbes} probes sent, {received} replies, {lost} lost, {lossPct:.1f}% loss')
print(f'timeouts fired: {timeouts}')
print(f'handshake = {handshakeMs:.3f} ms')
if rtts:
    print(f'rtt min/avg/max = {min(rtts):.3f}/{sum(rtts) / len(rtts):.3f}/{max(rtts):.3f} ms')
else:
    print('rtt min/avg/max = n/a (no replies)')
