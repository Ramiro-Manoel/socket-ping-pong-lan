import socket
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import UDP_PORT, REPETITIONS, SIZES

UDP_SIZES = [s for s in SIZES if s <= 65535]


def run(server_ip, size):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = b"x" * size
    rtts = []

    for _ in range(REPETITIONS):
        start = time.perf_counter()
        s.sendto(message, (server_ip, UDP_PORT))
        s.recvfrom(size)
        end = time.perf_counter()

        rtts.append((end - start) * 1000)

    s.close()
    return sum(rtts) / len(rtts)


def main(server_ip):
    results = []
    for size in UDP_SIZES:
        print(f"[UDP] Running {size} bytes...")
        rtt = run(server_ip, size)
        results.append((size, rtt))
        print(f"  RTT: {rtt:.3f} ms")
    return results


if __name__ == "__main__":
    main(sys.argv[1])
