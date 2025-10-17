import matplotlib.pyplot as plt

from motogp_dashboard import data_load
from motogp_dashboard import plot
from motogp_dashboard import animation
from motogp_dashboard import utils
from motogp_dashboard import config

def main():
    # Load and clean telemetry
    df = data_load.load_data()
    if df is None:
        return

    x = df['world_position_X']
    y = df['world_position_Y']

    # Smoothed break and throttle
    df['throttle_smooth'] = utils.smooth_and_limit(
        df['throttle'], df['dt'],
        alpha = config.SMOOTHING_ALPHA,
        rate_up = config.THR_RATE_UP, rate_down = config.THR_RATE_DOWN
    )
    df['brake_smooth'] = utils.smooth_and_limit(
        df['brake_0'], df['dt'],
        alpha = config.SMOOTHING_ALPHA,
        rate_up = config.BRK_RATE_UP, rate_down = config.BRK_RATE_DOWN
    )

    # Figure
    fig_ax = plot.setup_underlay(df, x, y, getattr(config, "TRACK_UNDERLAY", True))
    if fig_ax is None:
        fig, ax, dot = plot.init_plot(x, y)
    else:
        fig, ax, dot = fig_ax

    # HUD
    (
        left_fill, right_fill, lean_text,
        brk_rect, thr_rect, speed_text, gear_text,
        lap_text, laptime_text,
        bars_geo
    ) = plot.hud(fig, ax)

    # Animation
    animate = animation.make_animate(
        df, x, y, dot,
        left_fill, right_fill, lean_text,
        brk_rect, thr_rect, speed_text, gear_text,
        lap_text, laptime_text,
        bars_geo
    )
    n_frames = len(df)
    _ = animation.run_animation(fig, animate, n_frames, df)

    plt.show()

if __name__ == "__main__":
    main()
