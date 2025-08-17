"""
MotoGP 18 Telemetry Plotting and Dashboard Script
Author: Dennison Leadbetter-Clarke

This script reads telemetry data from a CSV file and generates visuals
for throttle, brake, RPM, gear, and a 2D track map.
"""

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection

# --- config and constants ---
DATA_DIR = 'data'
FILENAME = "example_lap.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)

# cleaning parameters
INTERPOLATE_LIMIT = 10  # only takes small gaps
JUMP_SIGMA = 5  # GPS jump cutoff = mean + JUMP_SIGMA * std

# timing
DT_PER_TICK = 0.01  # as binIndex is 100Hz
MIN_DT = 0.01  # avoid any freezes on 0
MAX_DT = 0.2  # avoid spikes

# overlay visuals
TRACK_SIZE = (8, 8)  # size of the track

THROTTLE_BAR_POSITION = [0.76, 0.55, 0.06, 0.35]  # [left, bottom, width, height]
BRAKE_BAR_POSITION = [0.90, 0.55, 0.06, 0.35]  # [left, bottom, width, height]

GEAR_POS = (0.02, 0.95)
RPM_POS = (0.02, 0.90)
THROTTLE_TXT_POS = (0.02, 0.85)
BRAKE_TXT_POS = (0.02, 0.80)

# colors
DOT_COLOR = 'red'
TRACK_COLOR = 'black'
TRAIL_COLOR = '#8000FF'  # bright violet
THROTTLE_COLOR = 'green'
BRAKE_COLOR = 'red'
RPM_COLOR = 'blue'
GEAR_COLOR = 'orange'

# --- load and clean ---
try:
    df = pd.read_csv(CSV_PATH, sep="\t")
    print(f"Loaded {len(df)} rows from '{FILENAME}'")

    # Drop any laps when lap is 0
    if 'lapIndex' in df.columns:
        race_rows = df['lapIndex'] > 0
        df = df[race_rows].reset_index(drop = True)

    # Throttle in [0, 1]
    df['throttle'] = df['throttle'].replace(-1.0, np.nan)
    df['throttle'] = df['throttle'].interpolate(limit = INTERPOLATE_LIMIT, limit_direction = 'both')
    df['throttle'] = df['throttle'].clip(lower = 0, upper = 1)

    # Brake in [0, 1]
    df['brake_0'] = df['brake_0'].replace(-1.0, np.nan)
    df['brake_0'] = df['brake_0'].interpolate(limit = INTERPOLATE_LIMIT, limit_direction = 'both')
    df['brake_0'] = df['brake_0'].clip(lower = 0, upper = 1)

    # RPM cleaning
    df['rpm'] = df['rpm'].replace(-1.0, np.nan)
    df['rpm'] = df['rpm'].interpolate(limit = INTERPOLATE_LIMIT, limit_direction = 'both')
    df['rpm'] = df['rpm'].clip(lower = 0)

    # Gear in [1, 6]
    df['gear'] = df['gear'].replace(-1, np.nan)
    df['gear'] = df['gear'].ffill().bfill()
    df['gear'] = df['gear'].round().clip(lower = 1, upper = 6)
    df['gear'] = df['gear'].astype(int)

    # Positions
    df['world_position_X'] = df['world_position_X'].replace(-1.0, np.nan)
    df['world_position_X'] = df['world_position_X'].interpolate(limit = INTERPOLATE_LIMIT, limit_direction = 'both')

    df['world_position_Y'] = df['world_position_Y'].replace(-1.0, np.nan)
    df['world_position_Y'] = df['world_position_Y'].interpolate(limit = INTERPOLATE_LIMIT, limit_direction = 'both')

    # Drop any rows still containing NaNs in required fields
    df = df.dropna(subset = [
        'world_position_X', 'world_position_Y',
        'throttle', 'brake_0', 'rpm', 'gear'
    ]).reset_index(drop = True)

    # removing jumps in GPS data for smoothness
    dx = df['world_position_X'].diff()
    dy = df['world_position_Y'].diff()
    distance = (dx**2 + dy**2) ** 0.5

    jump_threshold = distance.mean() + JUMP_SIGMA * distance.std()
    distance_no_nans = distance.fillna(0)
    valid_rows = distance_no_nans < jump_threshold

    df = df[valid_rows].copy()
    df.reset_index(drop = True, inplace = True)

    # timing
    bin_index_diff = df['binIndex'].diff()
    df['dt_raw'] = (bin_index_diff.fillna(1) * DT_PER_TICK).clip(lower=0) # raw dt
    df['dt'] = df['dt_raw'].clip(lower=MIN_DT, upper=MAX_DT) # clipped dt
    # lap time in seconds
    df['time_s'] = df['dt_raw'].cumsum()
    total_lap_time_s = float(df['time_s'].iloc[-1])

    # Cap the change in time to avoid strange animation spikes
    dt = df['dt']
    df['dt'] = df['dt'].clip(lower = MIN_DT, upper = MAX_DT)


except Exception as e:
    print(f"Failed to load or clean CSV: {e}")
    exit()

# --- animation --- 

n_frames = len(df)
x = df["world_position_X"]
y = df["world_position_Y"]

fig, ax = plt.subplots(figsize = TRACK_SIZE)
ax.plot(x, y, color = TRACK_COLOR, zorder = 0)

# trail
trail_len = 60
lc = LineCollection([], linewidths = 2.5, capstyle = 'round', zorder = 1, transform = ax.transData )
ax.add_collection(lc)

# marker for the current position
dot, = ax.plot([], [], 'o', color = DOT_COLOR, markersize = 10, zorder = 2)
ax.set_title("MotoGP18 Lap Simulation")

fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.axis("equal")
ax.grid(False)

# throttle and brake bars
throttle_ax = fig.add_axes(THROTTLE_BAR_POSITION)
brake_ax = fig.add_axes(BRAKE_BAR_POSITION)

# Throttle bar
throttle_bar = throttle_ax.bar([0], [0], width = 0.6, color = THROTTLE_COLOR)
throttle_ax.set_ylim(0, 1)
throttle_ax.set_xlim(-0.5, 0.5)
throttle_ax.set_xticks([])
throttle_ax.set_yticks([])
throttle_ax.set_title("Throttle", fontsize = 10)
for spine in throttle_ax.spines.values():
    spine.set_visible(False)

# Brake bar
brake_bar = brake_ax.bar([0], [0], width = 0.6, color = BRAKE_COLOR)
brake_ax.set_ylim(0, 1)
brake_ax.set_xlim(-0.5, 0.5)
brake_ax.set_xticks([])
brake_ax.set_yticks([])
brake_ax.set_title("Brake", fontsize = 10)
for spine in brake_ax.spines.values():
    spine.set_visible(False)

# Telemetry overlay
gear_text = ax.text(
    *GEAR_POS,
    '',
    transform = ax.transAxes,
    fontsize = 16,
    color = GEAR_COLOR,
    ha = 'left',
    va = 'top',
    bbox=dict(facecolor = 'white', edgecolor = GEAR_COLOR)
)

rpm_text = ax.text(
    *RPM_POS,
    '',
    transform = ax.transAxes,
    fontsize = 14,
    color = RPM_COLOR,
    ha = 'left',
    va = 'top',
    bbox=dict(facecolor = 'white', edgecolor = RPM_COLOR)
)

throttle_text = ax.text(
    *THROTTLE_TXT_POS,
    '',
    transform = ax.transAxes,
    fontsize = 14,
    color = THROTTLE_COLOR,
    ha = 'left',
    va = 'top',
    bbox = dict(facecolor = 'white', edgecolor = THROTTLE_COLOR)
)

brake_text = ax.text(
    *BRAKE_TXT_POS,
    '',
    transform = ax.transAxes,
    fontsize = 14,
    color = BRAKE_COLOR,
    ha = 'left',
    va = 'top',
    bbox = dict(facecolor = 'white', edgecolor = BRAKE_COLOR)
)

# Data animation
def animate(i):
    
    i0 = max(0, i - trail_len)

    xs = x.iloc[i0:i+1].to_numpy()
    ys = y.iloc[i0:i+1].to_numpy()

    if len(xs) >= 2:

        segs = np.stack([
            np.column_stack([xs[:-1], ys[:-1]]),
            np.column_stack([xs[1:],  ys[1: ]]),
        ], axis=1)

        base_rgba = mpl.colors.to_rgba(TRAIL_COLOR)
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

    gear_text.set_text(f"Gear: {gear}")
    rpm_text.set_text(f"RPM: {rpm}")
    throttle_text.set_text(f"Throttle: {throttle:.2f}")
    brake_text.set_text(f"Brake: {brake:.2f}")

    throttle_bar[0].set_height(throttle)
    brake_bar[0].set_height(brake)
    
    return dot, lc, gear_text, rpm_text, throttle_text, brake_text, throttle_bar[0], brake_bar[0]

# Use a fixed interval based on median dt (in ms)
interval_ms = int(1000 * df['dt'].median())

ani = animation.FuncAnimation(
    fig, animate, frames = n_frames,
    interval = interval_ms,
    blit = True, repeat = False
)

plt.show()