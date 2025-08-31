import numpy as np
import matplotlib as mpl
import matplotlib.animation as animation
from motogp_dashboard import utils, config

def run_animation(fig, animate, n_frames, df):
    interval_ms = int(1000 * df['dt'].median())
    ani = animation.FuncAnimation(
        fig, animate, frames = n_frames,
        interval = interval_ms,
        blit = True, repeat = False
    )
    return ani

def make_animate(df, x, y, dot, lc,
                 throttle_bar, brake_bar,
                 gear_text, rpm_text, throttle_text,
                 brake_text, speed_text, lap_text):

    def animate(i):
        # Fade trail
        i0 = max(0, i - config.TRAIL_LEN)
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

    return animate