# echo-client.py

import socket
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5001  # The port used by the server

arg=sys.argv[1]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(arg.encode())
    data = s.recv(1024)

print(f"Received {data!r}")
