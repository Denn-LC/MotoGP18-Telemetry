import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from motogp_dashboard import data_load
from motogp_dashboard import plot
from motogp_dashboard import animation
from motogp_dashboard import utils
from motogp_dashboard import config

def main():
    df = data_load.load_data()
    if df is None:
        return

    n_frames = len(df)
    x = df['world_position_X']
    y = df['world_position_Y']

    fig, ax, dot, lc = plot.init_plot(x, y)
    trail_len = 60

    # overlays (same as original script)
    throttle_ax = fig.add_axes(config.THROTTLE_BAR_POSITION)
    brake_ax = fig.add_axes(config.BRAKE_BAR_POSITION)

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

    def animate(i):
        i0 = max(0, i - trail_len)
        xs = x.iloc[i0:i+1].to_numpy()
        ys = y.iloc[i0:i+1].to_numpy()

        if len(xs) >= 2:
            segs = np.stack([np.column_stack([xs[:-1], ys[:-1]]),
                             np.column_stack([xs[1:], ys[1:]])], axis=1)
            base_rgba = mpl.colors.to_rgba(config.TRAIL_COLOR)
            alphas = np.linspace(0.05, 1.0, len(segs))
            colors = np.tile(base_rgba, (len(segs), 1))
            colors[:, 3] = alphas
            widths = np.linspace(1.5, 8, len(segs))
            lc.set_linewidths(widths)
            lc.set_segments(segs)
            lc.set_colors(colors)
        else:
            lc.set_segments([])

        dot.set_data([x.iloc[i]], [y.iloc[i]])

        gear = int(df['gear'].iloc[i])
        rpm = int(df['rpm'].iloc[i])
        throttle = df['throttle'].iloc[i]
        brake = df['brake_0'].iloc[i]
        speed_kph = df['speed_kph'].iloc[i]
        t_s = df['time_s'].iloc[i]

        lap_time_str = utils.format_time(t_s)

        gear_text.set_text(f"Gear: {gear}")
        rpm_text.set_text(f"RPM: {rpm}")
        throttle_text.set_text(f"Throttle: {throttle:.2f}")
        brake_text.set_text(f"Brake: {brake:.2f}")
        speed_text.set_text(f"Speed: {speed_kph:6.1f} km/h")
        lap_text.set_text(f"Lap time: {lap_time_str}")

        throttle_bar[0].set_height(throttle)
        brake_bar[0].set_height(brake)

        return (dot, lc, gear_text, rpm_text, throttle_text,
                brake_text, throttle_bar[0], brake_bar[0],
                speed_text, lap_text)

    ani = animation.run_animation(fig, animate, n_frames, df)
    plt.show()

if __name__ == "__main__":
    main()