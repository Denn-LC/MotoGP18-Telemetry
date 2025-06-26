"""
MotoGP 18 Telemetry Plotting and Dashboard Script
Author: Dennison Leadbetter-Clarke

This script reads telemetry data from a CSV file and generates visuals
for throttle, brake, RPM, gear, and a 2D track map.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import medfilt

# Configuration
DATA_DIR = 'data'
FILENAME = "example_lap.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)

# Load telemetry data
try:
    # Load from file
    df = pd.read_csv(CSV_PATH, sep="\t")
    print(f"Loaded {len(df)} rows from '{FILENAME}'")

    # Clip throttle and brake to [0, 1]
    df['throttle'] = df['throttle'].clip(lower=0, upper=1)
    df['brake_0'] = df['brake_0'].clip(lower=0, upper=1)

    # Save full dataset for 2D map (unfiltered)
    df_full = df.copy()

    # Create RPM/Gear safe copy for plotting
    df_rpm = df.copy()
    df_rpm = df_rpm.sort_values("binIndex").drop_duplicates(subset="binIndex")

    # Filter for valid RPM range
    df_rpm = df_rpm[(df_rpm["rpm"] > 5000) & (df_rpm["rpm"] < 17000)].copy()

    # Smooth RPM
    df_rpm["rpm_smooth"] = df_rpm["rpm"].rolling(window=20, center=True).mean()
    df_rpm.dropna(subset=["rpm_smooth"], inplace=True)

    # Cleanup gears
    df_rpm["gear_clean"] = df_rpm["gear"].ffill().astype(int)
    df_rpm["gear_clean"] = df_rpm["gear_clean"].where(df_rpm["rpm_smooth"] > 5000)
    df_rpm["gear_clean"] = df_rpm["gear_clean"].ffill()

except Exception as e:
    print(f"Failed to load CSV: {e}")
    exit()

# Plot 1: Throttle and Brake Over Time
# This plot uses the full dataset, since throttle/brake values don't require RPM filtering.

plt.figure(figsize=(10, 4))
plt.plot(df_full['binIndex'], df_full['throttle'], label='Throttle', color='green')
plt.plot(df_full['binIndex'], df_full['brake_0'], label='Brake', color='red')
plt.xlabel('Time (binIndex)')
plt.ylabel('Input (%)')
plt.title('Throttle and Brake vs Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/throttle_brake_vs_time.png")
plt.show()

# Plot 2: RPM and Gear over Time
# Uses filtered df_rpm to ensure clean and consistent data.

# Ensure data is sorted and unique by binIndex
df_rpm = df_rpm.sort_values("binIndex").drop_duplicates(subset="binIndex")

# Clean gear data
df_rpm["gear_clean"] = df_rpm["gear"].ffill().astype(int)
df_rpm["gear_clean"] = df_rpm["gear_clean"].where(df_rpm["rpm_smooth"] > 5000)
df_rpm["gear_clean"] = df_rpm["gear_clean"].ffill()

# Plot setup
fig, ax1 = plt.subplots(figsize=(10, 4))

# Plot RPM (blue)
ax1.plot(df_rpm["binIndex"], df_rpm["rpm_smooth"], label="RPM", color="blue")
ax1.set_ylabel("RPM", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Plot Gear (orange steps)
ax2 = ax1.twinx()
ax2.step(df_rpm["binIndex"], df_rpm["gear_clean"], where="post", color="orange", linestyle="--")
ax2.set_ylabel("Gear", color="orange")
ax2.tick_params(axis="y", labelcolor="orange")

# Final touches
plt.title("RPM and Gear vs Time")
plt.xlabel("Time (binIndex)")
fig.tight_layout()
plt.grid(True)
plt.savefig("plots/rpm_gear_vs_time.png")
plt.show()

# Plot 3: 2D Track Map (Top-Down View)

# Compute distances between each point and the previous one
dx = df_full['world_position_X'].diff()
dy = df_full['world_position_Y'].diff()
distance = (dx**2 + dy**2)**0.5

# Find index of the largest GPS jump
max_jump_idx = distance.idxmax()

# Slice data to only include points before the jump
df_map = df_full.loc[:max_jump_idx - 1]

# Plot the clean portion of the lap
plt.figure(figsize=(6, 6))
plt.plot(df_map["world_position_X"], df_map["world_position_Y"], color="purple")
plt.xlabel("World X Position")
plt.ylabel("World Y Position")
plt.title("2D Track Map (Top-Down View)")
plt.axis("equal")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/track_map.png")
plt.show()