import matplotlib.animation as animation

def run_animation(fig, animate, n_frames, df):
    interval_ms = int(1000 * df['dt'].median())
    ani = animation.FuncAnimation(
        fig, animate, frames = n_frames,
        interval = interval_ms,
        blit = True, repeat = False
    )
    return ani