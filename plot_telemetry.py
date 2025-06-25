"""
MotoGP 18 Telemetry Plotting and Dashboard Script
Author: Dennison Leadbetter-Clarke

This script reads telemetry data from a CSV file and generates visuals
for throttle, brake, RPM, gear, and a 2D track map.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
DATA_DIR = 'data'
FILENAME = "example_lap.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)

# Load telemetry data
try:
    df = pd.read_csv(CSV_PATH, sep = "\t")
    print(f" Loaded {len(df)} rows from '{FILENAME}'")
except Exception as e:
    print(f" Failed to load CSV: {e}")
    exit()

# Plot 1: Throttle and Brake Over Time
# This plot shows the throttle and brake inputs over time, binIndex functions as time.

plt.figure(figsize=(10, 4))
plt.plot(df['binIndex'], df['throttle'], label='Throttle', color='green')
plt.plot(df['binIndex'], df['brake_0'], label='Brake', color='red')
plt.xlabel('Time (binIndex)')
plt.ylabel('Input (%)')
plt.title('Throttle and Brake vs Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/throttle_brake_vs_time.png")
plt.show()

# Plot 2: RPM and Gear Over Time
plt.figure(figsize=(10, 4))
plt.plot(df["binIndex"], df["rpm"], label="RPM", color="blue")
plt.plot(df["binIndex"], df["gear"] * 1000, label="Gear × 1000", linestyle="--", color="orange")
plt.xlabel("Sample Index (binIndex)")
plt.ylabel("RPM / Gear")
plt.title("RPM and Gear vs Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/rpm_gear_vs_time.png")
plt.show()

# Plot 3: 2D Track Map
plt.figure(figsize=(6, 6))
plt.plot(df["world_position_X"], df["world_position_Y"], color="purple")
plt.xlabel("World X Position")
plt.ylabel("World Y Position")
plt.title("2D Track Map (Top-Down View)")
plt.axis("equal")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/track_map.png")
plt.show()