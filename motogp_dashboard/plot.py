import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from motogp_dashboard import config

def init_plot(x, y):
    fig, ax = plt.subplots(figsize = config.TRACK_SIZE)
    ax.plot(x, y, color = config.TRACK_COLOR, zorder = 0)

    lc = LineCollection([], linewidths = 2.5, capstyle = 'round',
                        zorder = 1, transform = ax.transData)
    ax.add_collection(lc)

    dot, = ax.plot([], [], 'o', color = config.DOT_COLOR,
                   markersize = 10, zorder = 2)
    ax.set_title("MotoGP18 Lap Simulation")

    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.tick_params(left = False, bottom = False,
                   labelleft = False, labelbottom = False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.axis("equal")
    ax.grid(False)

    return fig, ax, dot, lc