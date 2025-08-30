import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from motogp_dashboard import data_load
from motogp_dashboard import plot
from motogp_dashboard import animation
from motogp_dashboard import utils
from motogp_dashboard import config


def main():
    # Load
    df = data_load.load_data()
    if df is None:
        return

    # Shorthand series
    x = df['world_position_X']
    y = df['world_position_Y']
    n_frames = len(df)

    # Reset lap time when lapindex changes
    if 'lapIndex' in df.columns:
        df['lap_time_s'] = df['time_s'] - df.groupby('lapIndex')['time_s'].transform('min')
    else:
        df['lap_time_s'] = df['time_s']  # fallback if lapIndex missing

    # Smoothening

    def smooth_and_limit(series, dt, alpha, rate_up, rate_down):
    # EMA
        ema = series.ewm(alpha = alpha, adjust = False).mean().clip(0, 1)
    # Slew
        sig = ema.to_numpy()
        dtv = dt.to_numpy()

        out = np.empty_like(sig, dtype = float)
        out[0] = float(sig[0])
        for i in range(1, len(sig)):
            max_up   = rate_up   * float(dtv[i])
            max_down = rate_down * float(dtv[i])
            delta = sig[i] - out[i - 1]
            if delta > 0:
                delta = min(delta, max_up)
            else:
                delta = max(delta, -max_down)
            out[i] = out[i - 1] + delta
        return np.clip(out, 0.0, 1.0)

    # --- Throttle ---
    df['throttle_smooth'] = smooth_and_limit(df['throttle'], df['dt'],
                                            alpha = config.SMOOTHING_ALPHA,
                                            rate_up = config.THR_RATE_UP, rate_down = config.THR_RATE_DOWN ) 

    # --- Brake ---
    df['brake_smooth'] = smooth_and_limit(df['brake_0'], df['dt'],
                                         alpha = config.SMOOTHING_ALPHA,
                                         rate_up = config.BRK_RATE_UP, rate_down = config.BRK_RATE_DOWN )

    # Figure
    use_underlay = getattr(config, "TRACK_UNDERLAY", False) 

    if use_underlay and ('lapIndex' in df.columns):
        base_mask = (df['lapIndex'] == 1)
        if base_mask.any():
            x_base = x[base_mask]
            y_base = y[base_mask]
            fig, ax, dot, lc = plot.init_plot(x_base, y_base)

            for ln in list(ax.lines):
                if ln is not dot:
                    ln.set_linewidth(getattr(config, "TRACK_LINEWIDTH", 1.2))
                    ln.set_color(getattr(config, "TRACK_COLOR", (0.20, 0.20, 0.20)))
                    ln.set_alpha(getattr(config, "TRACK_ALPHA", 0.25))
        else:
            # Lap 1 not found then draw full session as base
            fig, ax, dot, lc = plot.init_plot(x, y)
    else:
        # Underlay disabled or lapIndex missing then draw full session as base
        fig, ax, dot, lc = plot.init_plot(x, y)

    # Overlays
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

    trail_len = getattr(config, "TRAIL_LEN", 60)

    def animate(i):
        # Fade trail
        i0 = max(0, i - trail_len)
        xs = x.iloc[i0:i+1].to_numpy()
        ys = y.iloc[i0:i+1].to_numpy()

        if len(xs) >= 2:
            segs = np.stack([
                np.column_stack([xs[:-1], ys[:-1]]),
                np.column_stack([xs[1:],  ys[1:]]),
            ], axis = 1)
            base_rgba = mpl.colors.to_rgba(config.TRAIL_COLOR)
            alphas = np.linspace(0.05, 1.0, len(segs))
            colors = np.tile(base_rgba, (len(segs), 1))
            colors[:, 3] = alphas
            widths = np.linspace(1.5, 8.0, len(segs))
            lc.set_linewidths(widths)
            lc.set_segments(segs)
            lc.set_colors(colors)
        else:
            lc.set_segments([])

        # Moving dot
        dot.set_data([x.iloc[i]], [y.iloc[i]])

        # Telemetry text + bars
        gear = int(df['gear'].iloc[i])
        rpm = int(df['rpm'].iloc[i])
        throttle = float(df['throttle_smooth'].iloc[i])
        brake = float(df['brake_smooth'].iloc[i])
        speed_kph = int(df['speed_kph'].iloc[i])

        # lap counter
        current_lap = int(df['lapIndex'].iloc[i])
        t_lap = float(df['lap_time_s'].iloc[i])
        lap_time_str = utils.format_time(t_lap)

        # Hud text
        lap_text.set_text(f"Lap {current_lap} | {lap_time_str}")
        gear_text.set_text(f"Gear: {gear}")
        rpm_text.set_text(f"RPM: {rpm}")
        throttle_text.set_text(f"Throttle: {throttle:.2f}")
        brake_text.set_text(f"Brake: {brake:.2f}")
        speed_text.set_text(f"Speed: {speed_kph} km/h")

        throttle_bar[0].set_height(throttle)
        brake_bar[0].set_height(brake)

        return (dot, lc, gear_text, rpm_text, throttle_text,
                brake_text, throttle_bar[0], brake_bar[0],
                speed_text, lap_text)

    # Run
    ani = animation.run_animation(fig, animate, n_frames, df)
    plt.show()


if __name__ == "__main__":
    main()
