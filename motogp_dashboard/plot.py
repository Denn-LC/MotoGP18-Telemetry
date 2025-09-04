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

def setup_underlay(df, x, y, use_underlay):
    if use_underlay and ('lapIndex' in df.columns):
        base_mask = (df['lapIndex'] == 1)
        if base_mask.any():
            x_base = x[base_mask]
            y_base = y[base_mask]
            fig, ax, dot, lc = init_plot(x_base, y_base)

            for ln in list(ax.lines):
                if ln is not dot:
                    ln.set_linewidth(getattr(config, "TRACK_LINEWIDTH", 1.2))
                    ln.set_color(getattr(config, "TRACK_COLOR", (0.20, 0.20, 0.20)))
                    ln.set_alpha(getattr(config, "TRACK_ALPHA", 0.25))
            return fig, ax, dot, lc
        
def hud(fig, ax):
    """
    Exact HUD setup lifted from main.py: throttle/brake bars and text labels.
    Returns all artists so main keeps the same variable names.
    """
    # Overlays (bars)
    throttle_ax = fig.add_axes(config.THROTTLE_BAR_POSITION)
    brake_ax    = fig.add_axes(config.BRAKE_BAR_POSITION)

    throttle_bar = throttle_ax.bar([0], [0], width = 0.6, color = config.THROTTLE_COLOR)
    throttle_ax.set_ylim(0, 1)
    throttle_ax.set_xlim(-0.5, 0.5)
    throttle_ax.set_xticks([]); throttle_ax.set_yticks([])
    throttle_ax.set_title("Throttle", fontsize = 10)
    for spine in throttle_ax.spines.values(): spine.set_visible(False)

    brake_bar = brake_ax.bar([0], [0], width = 0.6, color = config.BRAKE_COLOR)
    brake_ax.set_ylim(0, 1)
    brake_ax.set_xlim(-0.5, 0.5)
    brake_ax.set_xticks([]); brake_ax.set_yticks([])
    brake_ax.set_title("Brake", fontsize = 10)
    for spine in brake_ax.spines.values(): spine.set_visible(False)

    # Text overlays
    gear_text = ax.text(*config.GEAR_POS, '', transform = ax.transAxes,
                        fontsize = 16, color = config.GEAR_COLOR,
                        ha = 'left', va = 'top',
                        bbox = dict(facecolor = 'white', edgecolor = config.GEAR_COLOR))
    rpm_text = ax.text(*config.RPM_POS, '', transform = ax.transAxes,
                       fontsize = 14, color = config.RPM_COLOR,
                       ha = 'left', va = 'top',
                       bbox = dict(facecolor = 'white', edgecolor = config.RPM_COLOR))
    throttle_text = ax.text(*config.THROTTLE_TXT_POS, '', transform = ax.transAxes,
                            fontsize = 14, color = config.THROTTLE_COLOR,
                            ha = 'left', va = 'top',
                            bbox = dict(facecolor = 'white', edgecolor = config.THROTTLE_COLOR))
    brake_text = ax.text(*config.BRAKE_TXT_POS, '', transform = ax.transAxes,
                         fontsize = 14, color = config.BRAKE_COLOR,
                         ha = 'left', va = 'top',
                         bbox = dict(facecolor = 'white', edgecolor = config.BRAKE_COLOR))
    speed_text = ax.text(*config.SPEED_TXT_POS, '', transform = ax.transAxes,
                         fontsize = 14, color = 'black',
                         ha = 'left', va = 'top',
                         bbox = dict(facecolor = 'white', edgecolor = 'black'))
    lap_text = ax.text(*config.LAP_TXT_POS, '', transform = ax.transAxes,
                       fontsize = 14, color = 'black',
                       ha = 'left', va = 'top',
                       bbox = dict(facecolor = 'white', edgecolor = 'black'))
    lean_text = ax.text(*config.LEAN_TXT_POS, '', transform = ax.transAxes,
                    fontsize = 14, color = 'black',
                    ha = 'left', va = 'top',
                    bbox = dict(facecolor = 'white', edgecolor = 'black'))

    return throttle_bar, brake_bar, gear_text, rpm_text, throttle_text, brake_text, speed_text, lap_text, lean_text
