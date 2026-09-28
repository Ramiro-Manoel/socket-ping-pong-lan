import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


COLOR_TCP = "#2a78d6"
COLOR_UDP = "#eb6834"
SURFACE   = "#fcfcfb"
GRID      = "#e1e0d9"
INK       = "#0b0b0b"
INK_MUTED = "#898781"


def _format_size(size):
    if size >= 1_000_000:
        return f"{size // 1_000_000}MB"
    if size >= 1_000:
        return f"{size // 1_000}KB"
    return f"{size}B"


def generate(tcp_results, udp_results):
    tcp_sizes = [r[0] for r in tcp_results]
    tcp_rtts  = [r[1] for r in tcp_results]

    udp_sizes = [r[0] for r in udp_results]
    udp_rtts  = [r[1] for r in udp_results]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ax.plot(range(len(tcp_sizes)), tcp_rtts, color=COLOR_TCP, linewidth=2,
            marker="o", markersize=6, label="TCP")
    ax.plot(range(len(udp_sizes)), udp_rtts, color=COLOR_UDP, linewidth=2,
            marker="o", markersize=6, label="UDP")

    ax.set_xticks(range(len(tcp_sizes)))
    ax.set_xticklabels([_format_size(s) for s in tcp_sizes],
                       color=INK_MUTED, fontsize=10)

    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis="y", colors=INK_MUTED, labelsize=10)
    ax.tick_params(axis="x", length=0)

    ax.set_xlabel("Message size", color=INK_MUTED, fontsize=11, labelpad=8)
    ax.set_ylabel("RTT (ms)", color=INK_MUTED, fontsize=11, labelpad=8)
    ax.set_title("Round-Trip Time — TCP vs UDP", color=INK, fontsize=13, pad=14)

    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.grid(axis="y", which="minor", color=GRID, linewidth=0.4, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(frameon=False, labelcolor=INK, fontsize=11)

    plt.tight_layout()
    plt.savefig("rtt_chart.png", dpi=150, facecolor=SURFACE)
    plt.show()
    print("Chart saved to rtt_chart.png")


def generate_bandwidth(tcp_results, udp_results):
    def to_bandwidth(results):
        return [(size, (size / 1e6) / (rtt / 1000)) for size, rtt in results]

    tcp_bw = to_bandwidth(tcp_results)
    udp_bw = to_bandwidth(udp_results)

    tcp_sizes = [r[0] for r in tcp_bw]
    tcp_vals  = [r[1] for r in tcp_bw]
    udp_sizes = [r[0] for r in udp_bw]
    udp_vals  = [r[1] for r in udp_bw]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    ax.plot(range(len(tcp_sizes)), tcp_vals, color=COLOR_TCP, linewidth=2,
            marker="o", markersize=6, label="TCP")
    ax.plot(range(len(udp_sizes)), udp_vals, color=COLOR_UDP, linewidth=2,
            marker="o", markersize=6, label="UDP")

    ax.set_xticks(range(len(tcp_sizes)))
    ax.set_xticklabels([_format_size(s) for s in tcp_sizes],
                       color=INK_MUTED, fontsize=10)

    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis="y", colors=INK_MUTED, labelsize=10)
    ax.tick_params(axis="x", length=0)

    ax.set_xlabel("Message size", color=INK_MUTED, fontsize=11, labelpad=8)
    ax.set_ylabel("Bandwidth (MB/s)", color=INK_MUTED, fontsize=11, labelpad=8)
    ax.set_title("Bandwidth — TCP vs UDP", color=INK, fontsize=13, pad=14)

    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.grid(axis="y", which="minor", color=GRID, linewidth=0.4, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(frameon=False, labelcolor=INK, fontsize=11)

    plt.tight_layout()
    plt.savefig("bandwidth_chart.png", dpi=150, facecolor=SURFACE)
    plt.show()
    print("Chart saved to bandwidth_chart.png")
