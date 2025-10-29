import pandas as pd
import numpy as np
from motogp_dashboard import config

def add_lean_angle(df):
    # Calculate lean angle (degrees) from telemetry world positions
    x = df['world_position_X'].astype('float64').to_numpy()
    y = df['world_position_Y'].astype('float64').to_numpy()
    t = df['time_s'].astype('float64').to_numpy()

    # enforce monotonically increasing time
    t = t + np.arange(len(t)) * 1e-9

    dt = np.diff(t, prepend = t[0])
    med = np.nanmedian(dt)
    dt_med = float(med) if np.isfinite(med) and med > 0 else 1.0 / 60.0

    # smoothing on positions
    w_pos = int(round(config.POS_SMOOTH_S / dt_med))
    if w_pos < 5: w_pos = 5
    if w_pos % 2 == 0: w_pos += 1

    xs = pd.Series(x).rolling(window = w_pos, center = True, min_periods = 1).median() \
                     .rolling(window = w_pos, center = True, min_periods = 1).mean().to_numpy()
    ys = pd.Series(y).rolling(window = w_pos, center = True, min_periods = 1).median() \
                     .rolling(window = w_pos, center = True, min_periods = 1).mean().to_numpy()

    dx = np.gradient(xs, t, edge_order = 2)
    dy = np.gradient(ys, t, edge_order = 2)
    ddx = np.gradient(dx,  t, edge_order = 2)
    ddy = np.gradient(dy,  t, edge_order = 2)

    v2   = dx * dx + dy * dy
    denom = np.power(np.maximum(v2, 1e-12), 1.5)
    kappa = (dx * ddy - dy * ddx) / denom
    kappa = np.nan_to_num(kappa, nan = 0.0, posinf = 0.0, neginf = 0.0)

    speed = df['speed_mps'].astype('float64').to_numpy()

    a_lat = (speed ** 2) * kappa
    phi_rad = np.arctan2(a_lat, 9.81)
    lean_deg = np.degrees(phi_rad)

    # Clean up nans, low speed and clip
    lean_deg[speed < float(config.MIN_SPEED_MS)] = 0.0
    lean_deg = np.clip(lean_deg, -float(config.MAX_DEG), float(config.MAX_DEG))
    lean_deg = np.nan_to_num(lean_deg, nan = 0.0, posinf = 0.0, neginf = 0.0)

    # final smoothing
    w_lean = int(round(config.LEAN_SMOOTH_S / dt_med))
    if w_lean < 7: w_lean = 7
    if w_lean % 2 == 0: w_lean += 1

    lean_deg = pd.Series(lean_deg).rolling(window = 5, center = True, min_periods = 1).median() \
                                 .rolling(window = w_lean, center = True, min_periods = 1).mean().to_numpy()

    df['lean_deg_signed'] = lean_deg
    df['lean_deg'] = np.abs(lean_deg)
    return df

def add_lap_time(df):
    df['lapIndex'] = df['lapIndex'].round().astype('Int64').ffill().bfill().astype(int)
    df['lap_time_s'] = df.groupby('lapIndex')['dt'].cumsum().shift(fill_value = 0.0)
    return df

def load_data():
    try:
        df = pd.read_csv(config.CSV_PATH, sep = "\t")
        print(f"Loaded {len(df)} rows from '{config.FILENAME}'")

        # Inputs
        df['throttle'] = df['throttle'].replace(-1.0, np.nan).interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both').clip(0, 1)
        df['brake_0'] = df['brake_0'].replace(-1.0, np.nan).interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both').clip(0, 1)
        # RPM kept for possible future use
        df['rpm'] = df['rpm'].replace(-1.0, np.nan).interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both').clip(lower = 0)

        df['gear'] = df['gear'].replace(-1, np.nan).ffill().bfill().round().clip(1, 6).astype(int)

        df['world_position_X'] = df['world_position_X'].replace(-1.0, np.nan).interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')
        df['world_position_Y'] = df['world_position_Y'].replace(-1.0, np.nan).interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')

        df = df.dropna(subset = ['world_position_X', 'world_position_Y', 'throttle', 'brake_0', 'rpm', 'gear']).reset_index(drop = True)

        # Remove GPS jumps
        dx = df['world_position_X'].diff()
        dy = df['world_position_Y'].diff()
        distance = (dx**2 + dy**2) ** 0.5
        jump_threshold = distance.mean() + config.JUMP_SIGMA * distance.std()
        df = df[distance.fillna(0) < jump_threshold].reset_index(drop = True)

        # Timing
        bin_index_diff = df['binIndex'].diff()
        df['dt_raw'] = (bin_index_diff.fillna(1) * config.DT_PER_TICK).clip(lower = 0)
        df['dt'] = df['dt_raw'].clip(lower = config.MIN_DT, upper = config.MAX_DT)
        df['time_s'] = df['dt_raw'].cumsum()

        # Speed
        vx = df['velocity_X']; vy = df['velocity_Y']; vz = df['velocity_Z']
        df['speed_mps'] = np.sqrt(vx**2 + vy**2 + vz**2)
        df['speed_kph'] = df['speed_mps'] * 3.6

        df = add_lean_angle(df)
        df = add_lap_time(df)

        return df

    except Exception as e:
        print(f"Failed to load or clean CSV: {e}")
        return None
