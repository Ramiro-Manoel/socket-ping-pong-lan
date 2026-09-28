import socket
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import UDP_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", UDP_PORT))
print(f"UDP waiting on port {UDP_PORT}...")

while True:
    data, addr = s.recvfrom(65535)
    s.sendto(data, addr)