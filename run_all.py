import sys
from src.config import TCP_PORT, UDP_PORT
from src.client import tcp, udp
from src import plot

server_ip = sys.argv[1]

try:
    tcp_results = tcp.main(server_ip)
except (ConnectionRefusedError, TimeoutError):
    print(f"Error: could not connect to TCP server at {server_ip}:{TCP_PORT}")
    print("Make sure src/server/tcp.py is running on the remote machine.")
    sys.exit(1)

try:
    udp_results = udp.main(server_ip)
except OSError:
    print(f"Error: could not reach UDP server at {server_ip}:{UDP_PORT}")
    print("Make sure src/server/udp.py is running on the remote machine.")
    sys.exit(1)


def _bw(size, rtt_ms):
    return (size / 1e6) / (rtt_ms / 1000)


def _fmt(size):
    if size >= 1_000_000: return f"{size // 1_000_000}MB"
    if size >= 1_000:     return f"{size // 1_000}KB"
    return f"{size}B"


udp_map = {size: rtt for size, rtt in udp_results}

print("\nResults summary:")
print(f"  {'Size':<10} {'TCP RTT':>10} {'TCP BW':>12} {'UDP RTT':>10} {'UDP BW':>12}")
print(f"  {'-'*10} {'-'*10} {'-'*12} {'-'*10} {'-'*12}")
for size, rtt_tcp in tcp_results:
    rtt_udp = udp_map.get(size)
    bw_tcp  = f"{_bw(size, rtt_tcp):.3f} MB/s"
    if rtt_udp:
        bw_udp  = f"{_bw(size, rtt_udp):.3f} MB/s"
        udp_rtt = f"{rtt_udp:.3f} ms"
    else:
        bw_udp  = "N/A"
        udp_rtt = "N/A"
    print(f"  {_fmt(size):<10} {rtt_tcp:>7.3f} ms {bw_tcp:>12} {udp_rtt:>10} {bw_udp:>12}")

plot.generate(tcp_results, udp_results)
plot.generate_bandwidth(tcp_results, udp_results)
