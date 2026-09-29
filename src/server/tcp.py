import socket
import struct
from src.config import TCP_PORT
from src.utils import recv_all


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", TCP_PORT))
s.listen(1)
print(f"TCP waiting on port {TCP_PORT}...")

while True:
    conn, addr = s.accept()
    print(f"Connected: {addr}")

    while True:
        header = recv_all(conn, 8)
        if not header:
            break
        size = struct.unpack("!Q", header)[0]

        data = recv_all(conn, size)
        conn.send(header + data)

    conn.close()