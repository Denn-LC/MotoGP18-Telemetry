"""
MotoGP 18 Telemetry Plotting and Dashboard Script
Author: Dennison Leadbetter-Clarke

This script reads telemetry data from a CSV file and generates visuals
for throttle, brake, RPM, gear, and a 2D track map.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Configuration
DATA_DIR = 'data'
FILENAME = "example_lap.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)

# Taking in data and cleaning
try:
    df = pd.read_csv(CSV_PATH, sep="\t")
    print(f"Loaded {len(df)} rows from '{FILENAME}'")

    # Clean up invalid placeholders, e.g -1.0 for throttle/brake, -1 for gear
    df['throttle'] = df['throttle'].replace(-1.0, np.nan).clip(upper=1)
    df['brake_0'] = df['brake_0'].replace(-1.0, np.nan).clip(upper=1)
    df['rpm'] = df['rpm'].replace(-1.0, np.nan)
    df['gear'] = df['gear'].replace(-1, np.nan)
    df['world_position_X'] = df['world_position_X'].replace(-1.0, np.nan)
    df['world_position_Y'] = df['world_position_Y'].replace(-1.0, np.nan)

    # Interpolating data to fill gaps and clean
    df['throttle'] = df['throttle'].interpolate(limit=10, limit_direction='both')
    df['brake_0'] = df['brake_0'].interpolate(limit=10, limit_direction='both')
    df['rpm'] = df['rpm'].interpolate(limit=10, limit_direction='both')
    df['gear'] = df['gear'].ffill().bfill().clip(lower=1, upper=6)
    df['world_position_X'] = df['world_position_X'].interpolate(limit=10, limit_direction='both')
    df['world_position_Y'] = df['world_position_Y'].interpolate(limit=10, limit_direction='both')

    # Remove rows with any remaining NaNs
    df = df.dropna(subset=['world_position_X', 'world_position_Y', 'throttle', 'brake_0', 'rpm', 'gear'])

    # removing jumps in GPS data for smoothness
    dx = df['world_position_X'].diff()
    dy = df['world_position_Y'].diff()
    distance = (dx**2 + dy**2)**0.5
    jump_threshold = distance.mean() + 5 * distance.std()
    df = df[distance.fillna(0) < jump_threshold]
    df = df.reset_index(drop=True)

    # Calculate change in time using binIndex
    df['dt'] = df['binIndex'].diff().fillna(0) * 0.01

    # Cap the change in time to avoid strange animation spikes
    df['dt'] = df['dt'].clip(lower=0.01, upper=0.2)

except Exception as e:
    print(f"Failed to load or clean CSV: {e}")
    exit()

# Animated lap simulation

n_frames = len(df)
x = df["world_position_X"]
y = df["world_position_Y"]

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(x, y, color="purple", alpha=0.3)
dot, = ax.plot([], [], 'ro', markersize=10)
ax.set_title("MotoGP18 Lap Simulation")

fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.axis("equal")
ax.grid(False)

# throttle and brake bars
throttle_ax = fig.add_axes([0.76, 0.55, 0.06, 0.35])  # [left, bottom, width, height]
brake_ax = fig.add_axes([0.90, 0.55, 0.06, 0.35])

# Throttle bar
throttle_bar = throttle_ax.bar([0], [0], width=0.6, color='green')
throttle_ax.set_ylim(0, 1)
throttle_ax.set_xlim(-0.5, 0.5)
throttle_ax.set_xticks([])
throttle_ax.set_yticks([])
throttle_ax.set_title("Throttle", fontsize=10)
for spine in throttle_ax.spines.values():
    spine.set_visible(False)

# Brake bar
brake_bar = brake_ax.bar([0], [0], width=0.6, color='red')
brake_ax.set_ylim(0, 1)
brake_ax.set_xlim(-0.5, 0.5)
brake_ax.set_xticks([])
brake_ax.set_yticks([])
brake_ax.set_title("Brake", fontsize=10)
for spine in brake_ax.spines.values():
    spine.set_visible(False)

# Telemetry overlay
gear_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=16, color='orange', ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='orange'))
rpm_text = ax.text(0.02, 0.90, '', transform=ax.transAxes, fontsize=14, color='blue', ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='blue'))
throttle_text = ax.text(0.02, 0.85, '', transform=ax.transAxes, fontsize=14, color='green', ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='green'))
brake_text = ax.text(0.02, 0.80, '', transform=ax.transAxes, fontsize=14, color='red', ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='red'))

# Data animation
def animate(i):
    dot.set_data([x.iloc[i]], [y.iloc[i]])
    gear = int(df['gear'].iloc[i])
    rpm = int(df['rpm'].iloc[i])
    throttle = df['throttle'].iloc[i]
    brake = df['brake_0'].iloc[i]
    gear_text.set_text(f"Gear: {gear}")
    rpm_text.set_text(f"RPM: {rpm}")
    throttle_text.set_text(f"Throttle: {throttle:.2f}")
    brake_text.set_text(f"Brake: {brake:.2f}")
    
    # Update bar heights
    throttle_bar[0].set_height(throttle)
    brake_bar[0].set_height(brake)
    return dot, gear_text, rpm_text, throttle_text, brake_text, throttle_bar[0], brake_bar[0]

# Use a fixed interval based on median dt (in ms)
interval_ms = int(1000 * df['dt'].median())

ani = animation.FuncAnimation(
    fig, animate, frames=n_frames,
    interval=interval_ms,
    blit=True, repeat=False
)

# Remove tight_layout to avoid the warning with inset axes
# plt.tight_layout()
plt.show()