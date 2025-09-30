import numpy as np
import pandas as pd

def format_time(t_s):
    mins = int(t_s // 60)
    secs = t_s - 60 * mins

    return f"{mins:d}:{secs:06.3f}"

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


