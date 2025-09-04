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

    df = data_load.add_lap_time(df)

    # --- Throttle ---
    df['throttle_smooth'] = utils.smooth_and_limit(df['throttle'], df['dt'],
                                            alpha = config.SMOOTHING_ALPHA,
                                            rate_up = config.THR_RATE_UP, rate_down = config.THR_RATE_DOWN ) 

    # --- Brake ---
    df['brake_smooth'] = utils.smooth_and_limit(df['brake_0'], df['dt'],
                                        alpha = config.SMOOTHING_ALPHA,
                                        rate_up = config.BRK_RATE_UP, rate_down = config.BRK_RATE_DOWN )

    # Figure
    use_underlay = getattr(config, "TRACK_UNDERLAY", False)
    fig, ax, dot, lc = plot.setup_underlay(df, x, y, use_underlay)

    # HUD
    (throttle_bar, brake_bar, gear_text, rpm_text, throttle_text,
    brake_text, speed_text, lap_text, lean_text) = plot.hud(fig, ax)

    # Animation
    animate = animation.make_animate(
    df, x, y, dot, lc,
    throttle_bar, brake_bar,
    gear_text, rpm_text, throttle_text,
    brake_text, speed_text, lap_text, lean_text
)
    n_frames = len(df)
    ani = animation.run_animation(fig, animate, n_frames, df)
    plt.show()

if __name__ == "__main__":
    main()
