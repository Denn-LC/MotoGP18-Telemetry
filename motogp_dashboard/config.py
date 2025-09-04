import os

# ----------------------------
# File paths
# ----------------------------
DATA_DIR  = 'data'
FILENAME  = 'new_example.csv'
CSV_PATH  = os.path.join(DATA_DIR, FILENAME)

# ----------------------------
# Cleaning parameters
# ----------------------------
INTERPOLATE_LIMIT = 10     # only fill small gaps
JUMP_SIGMA        = 5      # GPS jump cutoff = mean + JUMP_SIGMA * std
SMOOTHING_ALPHA   = 0.15   # 0 < alpha <= 1, higher = less smoothing

THR_RATE_UP   = 3.0   # throttle can rise fast
THR_RATE_DOWN = 5.0   # can close even faster
BRK_RATE_UP   = 6.0   # brake can bite quickly
BRK_RATE_DOWN = 4.0   # and release fast(ish)

# ----------------------------
# Timing
# ----------------------------
DT_PER_TICK = 0.01         # binIndex is 100 Hz
MIN_DT      = 0.01         # avoid freezes on 0
MAX_DT      = 0.20         # avoid spikes

# ----------------------------
# Figure / track
# ----------------------------
TRACK_SIZE      = (6, 6)   # overall figure size (used by plot.init_plot, if wired)
TRACK_UNDERLAY  = True     # draw lap 1 as light base map

# Underlay style
TRACK_COLOR     = (0.20, 0.20, 0.20)  # light grey for the base lap line
TRACK_ALPHA     = 0.25
TRACK_LINEWIDTH = 1.2

# ----------------------------
# HUD overlay positions
# ----------------------------
THROTTLE_BAR_POSITION = [0.76, 0.55, 0.06, 0.35]
BRAKE_BAR_POSITION    = [0.90, 0.55, 0.06, 0.35]

# Text overlays anchored to ax.transAxes
GEAR_POS          = (0.02, 0.95)
RPM_POS           = (0.02, 0.89)
THROTTLE_TXT_POS  = (0.02, 0.83)
BRAKE_TXT_POS     = (0.02, 0.77)
SPEED_TXT_POS     = (0.02, 0.71)
LAP_TXT_POS       = (0.02, 0.65)
LEAN_TXT_POS      = (0.02, 0.59)

# ----------------------------
# Animation
# ----------------------------
TRAIL_LEN = 60

# ----------------------------
# Colors 
# ----------------------------
DOT_COLOR      = 'red'
TRAIL_COLOR    = '#8000FF'
THROTTLE_COLOR = 'green'
BRAKE_COLOR    = 'red'
RPM_COLOR      = 'blue'
GEAR_COLOR     = 'orange'
