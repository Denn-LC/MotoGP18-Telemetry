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
INTERPOLATE_LIMIT = 10
JUMP_SIGMA        = 5
SMOOTHING_ALPHA   = 0.15

THR_RATE_UP   = 7.0
THR_RATE_DOWN = 9.0
BRK_RATE_UP   = 7.0
BRK_RATE_DOWN = 9.0

MIN_SPEED_MS  = 3.0
MAX_DEG       = 70.0
POS_SMOOTH_S  = 0.12
LEAN_SMOOTH_S = 0.25

# ----------------------------
# Timing
# ----------------------------
DT_PER_TICK = 0.01
MIN_DT      = 0.01
MAX_DT      = 0.20

# ----------------------------
# Figure / track
# ----------------------------
TRACK_SIZE      = (6.8, 6.8)
TRACK_UNDERLAY  = True
TRACK_COLOR     = (0.20, 0.20, 0.20)
TRACK_ALPHA     = 0.25
TRACK_LINEWIDTH = 1.2
SUBPLOT_BOTTOM  = 0.44 # Reserve space for the track map

# ----------------------------
# HUD layout
# ----------------------------
# [left, bottom, width, height]
HUD_BOX_POS   = [0.33, 0.10, 0.34, 0.35]

LEAN_AX_REL   = [0.15, 0.56, 0.70, 0.35]
BARS_AX_REL   = [0.10, 0.50, 0.80, 0.09]

SPEED_POS_REL = (0.50, 0.42)
GEAR_POS_REL  = (0.50, 0.28)

LAP_POS_REL     = (0.10, 0.15)
LAPTIME_POS_REL = (0.90, 0.15)

HUD_BG           = True                 # toggle panel
HUD_BG_COLOR     = (0.12, 0.12, 0.12)   # dark grey
HUD_BG_ALPHA     = 0.90
HUD_BG_ROUND_FRAC = 0.1 # size of the rounded corners
HUD_BG_INSET_X   = 0.06
HUD_BG_INSET_Y   = 0.06
BEZIER_KAPPA     = 0.5522847498307936

# Grey outline geometry
GAP_FRAC   = 0.04
HALF_FRAC  = 0.5
LEFT_X0    = 0.0
LEFT_X1    = HALF_FRAC - (GAP_FRAC * 0.5)
LEFT_DIFF  = LEFT_X1 - LEFT_X1
RIGHT_X0   = HALF_FRAC + (GAP_FRAC * 0.5)
RIGHT_X1   = 1.0
RIGHT_DIFF = RIGHT_X1 - RIGHT_X0

BAR_H = 0.52
BAR_Y = 0.5 - (BAR_H * 0.5)

# Lean geometry
LEAN_ARC_RADIUS    = 1.00
LEAN_ARC_LINEWIDTH = 8
LEAN_FILL_WIDTH    = 0.18
LEAN_EDGE_PAD_DEG  = 0.8
LEAN_X_PAD         = 0.06
LEAN_Y_PAD         = 0.06

# Text and fonts
FONT_PATH       = None
FONT_FALLBACK   = 'DejaVu Sans'
FONT_SIZE_SPEED = 24
FONT_SIZE_GEAR  = 18
FONT_SIZE_LEAN  = 21
FONT_SIZE_META  = 13
FONT_WEIGHT     = 'normal'
STROKE_W        = 1.0
STROKE_ALPHA    = 0.85

# Colors
DOT_COLOR      = 'red'
THROTTLE_COLOR = 'green'
BRAKE_COLOR    = 'red'

# Lean visuals
LEAN_RING_BG    = (0.75, 0.75, 0.75)
LEAN_FILL_COLOR = (1.00, 0.85, 0.15)
TEXT_COLOR      = 'black'

# Lean color thresholds (deg)
LEAN_LOW_DEG   = 25
LEAN_HIGH_DEG  = 50

LEAN_COLOR_LOW  = (1.0, 1.0, 1.0)
LEAN_COLOR_MID  = (1.00, 0.85, 0.15)
LEAN_COLOR_HIGH = (0.90, 0.20, 0.20)