import socket
import struct
import sys
import time
from src.config import TCP_PORT, REPETITIONS, SIZES
from src.utils import recv_all


def run(server_ip, size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, TCP_PORT))

    message = b"x" * size
    header = struct.pack("!Q", size)
    rtts = []

    for _ in range(REPETITIONS):
        start = time.perf_counter()
        s.send(header + message)
        recv_all(s, 8 + size)
        end = time.perf_counter()

        rtts.append((end - start) * 1000)

    s.close()
    return sum(rtts) / len(rtts)


def main(server_ip):
    results = []
    for size in SIZES:
        print(f"[TCP] Running {size} bytes...")
        rtt = run(server_ip, size)
        results.append((size, rtt))
        print(f"  RTT: {rtt:.3f} ms")
    return results


if __name__ == "__main__":
    main(sys.argv[1])
