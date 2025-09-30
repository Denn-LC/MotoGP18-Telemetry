import numpy as np
import matplotlib.animation as mpl_animation
from motogp_dashboard import config
from motogp_dashboard import utils

def run_animation(fig, animate, n_frames, df):
    # Determine interval from median dt to get real time animation
    interval_ms = int(1000 * df['dt'].median())
    ani = mpl_animation.FuncAnimation(
        fig, animate, frames = n_frames,
        interval = interval_ms, blit = True, repeat = False
    )
    return ani

def make_animate(df, x, y, dot,
                 left_fill, right_fill, lean_text,
                 brk_rect, thr_rect, speed_text, gear_text,
                 lap_text, laptime_text,
                 bars_geo):
    # builds animation function
    max_deg = float(config.MAX_DEG)

    def lean_colour(mag_deg):
        if mag_deg <= float(config.LEAN_LOW_DEG):
            return config.LEAN_COLOR_LOW
        if mag_deg >= float(config.LEAN_HIGH_DEG):
            return config.LEAN_COLOR_HIGH
        return config.LEAN_COLOR_MID

    def update_lean(lean_ang):
        # Fill arc and text for lean angle
        edge_pad = float(bars_geo.get('edge_pad_deg', 0.0))
        theta_min = 0.0 + edge_pad
        theta_max = 180.0 - edge_pad

        mag  = min(abs(float(lean_ang)), max_deg)
        span = 90.0 * (mag / max_deg)

        col = lean_colour(mag)

        # Reset both wedges
        left_fill.set_theta1(90);  left_fill.set_theta2(90)
        right_fill.set_theta1(90); right_fill.set_theta2(90)

        left_fill.set_facecolor(col)
        right_fill.set_facecolor(col)
        lean_text.set_color(col)

        if lean_ang >= 0:
            t1 = max(90.0 - span, theta_min)
            right_fill.set_theta1(t1)
            right_fill.set_theta2(90.0)
        else:
            t2 = min(90.0 + span, theta_max)
            left_fill.set_theta1(90.0)
            left_fill.set_theta2(t2)

        lean_text.set_text(f"{int(round(mag))}°")

    def brk_thr_bars(brake, throttle):
        # Update brake and throttle bars
        brk_rect.set_facecolor(config.BRAKE_COLOR)
        thr_rect.set_facecolor(config.THROTTLE_COLOR)

        brake    = max(0.0, min(1.0, float(brake)))
        throttle = max(0.0, min(1.0, float(throttle)))

        left_edge   = bars_geo['left_edge']
        left_min    = bars_geo['left_min']
        right_edge  = bars_geo['right_edge']
        right_max   = bars_geo['right_max']
        bar_y       = bars_geo['bar_y']
        bar_h       = bars_geo['bar_h']

        # Brake grows to the left
        max_left_width = left_edge - left_min
        brk_w = max_left_width * brake
        brk_rect.set_x(left_edge - brk_w)
        brk_rect.set_y(bar_y)
        brk_rect.set_width(brk_w)
        brk_rect.set_height(bar_h)

        # Throttle grows to the right
        max_right_width = right_max - right_edge
        thr_w = max_right_width * throttle
        thr_rect.set_x(right_edge)
        thr_rect.set_y(bar_y)
        thr_rect.set_width(thr_w)
        thr_rect.set_height(bar_h)

    def animate(i):
        # Track position
        dot.set_data([x.iloc[i]], [y.iloc[i]])

        # Readouts
        throttle  = df['throttle_smooth'].iloc[i]
        brake     = df['brake_smooth'].iloc[i]
        speed_kph = int(df['speed_kph'].iloc[i])
        gear      = int(df['gear'].iloc[i])

        # Lean angle
        lean_ang = df['lean_deg_signed'].iloc[i]

        # Lap and live lap time
        lap_val = int(df['lapIndex'].iloc[i])
        t_s     = float(df['lap_time_s'].iloc[i])
        lap_text.set_text(f"Lap {lap_val}")
        laptime_text.set_text(utils.format_time(t_s))

        brk_thr_bars(brake, throttle)
        update_lean(lean_ang)
        speed_text.set_text(f"{speed_kph}km/h")
        gear_text.set_text(f"{gear}")

        return (
            dot, brk_rect, thr_rect,
            left_fill, right_fill, lean_text,
            speed_text, gear_text, lap_text, laptime_text
        )

    return animate
