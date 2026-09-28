# Socket Ping-Pong LAN

Measures round-trip time (RTT) and bandwidth between two physical machines on a LAN using raw TCP and UDP sockets. Sends messages of varying sizes, collects latency averages over multiple repetitions, and generates charts for comparison.

## Requirements

- Python 3.8+
- `pip install -r requirements.txt`
- Two physical machines on the same LAN (no VMs, no loopback)

## Project structure

```
run_all.py          — entry point
src/
  config.py         — message sizes, ports, repetitions
  utils.py          — shared recv_all helper
  plot.py           — chart generation
  server/
    tcp.py          — TCP echo server
    udp.py          — UDP echo server
  client/
    tcp.py          — TCP RTT measurement
    udp.py          — UDP RTT measurement
```

## How to run

**Machine B (server)** — open two terminals:

```
python src/server/tcp.py
python src/server/udp.py
```

**Machine A (client)**:

```
python run_all.py <server-ip>
```

Example:

```
python run_all.py 192.168.1.10
```

Results are printed to the terminal and two charts are saved:

- `rtt_chart.png` — round-trip time per message size
- `bandwidth_chart.png` — bandwidth per message size

## Configuration

Edit `config.py` to change ports, message sizes, or number of repetitions:

```python
TCP_PORT    = 5000
UDP_PORT    = 5001
REPETITIONS = 100
SIZES       = [100, 500, 1024, 512000, 1048576, 10485760]
```

## Notes

- UDP does not support messages larger than 65535 bytes — sizes above that are TCP-only.
- RTT values are averages over `REPETITIONS` round trips per message size.
