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

# Reserve bottom space so the track map and dash never overlap
SUBPLOT_BOTTOM  = 0.4
# ----------------------------
# HUD layout
# ----------------------------

# [left, bottom, width, height]

HUD_BOX_POS   = [0.33, 0.10, 0.34, 0.35]   

LEAN_AX_REL   = [0.15, 0.56, 0.70, 0.35]   
BARS_AX_REL   = [0.10, 0.5, 0.80, 0.09]   

SPEED_POS_REL = (0.50, 0.42)           
GEAR_POS_REL  = (0.50, 0.28)             

LAP_POS_REL     = (0.1, 0.15)         
LAPTIME_POS_REL = (0.9, 0.15)        

# ----------------------------
# Lean geometry
# ----------------------------
LEAN_ARC_RADIUS    = 1.00
LEAN_ARC_LINEWIDTH = 8
LEAN_FILL_WIDTH    = 0.18
LEAN_EDGE_PAD_DEG  = 0.8   # avoid exact 0° and 180° to prevent raster clipping
LEAN_X_PAD         = 0.06
LEAN_Y_PAD         = 0.06

# ----------------------------
# Text and fonts
# ----------------------------
FONT_PATH       = None
FONT_FALLBACK   = 'DejaVu Sans'
FONT_SIZE_SPEED = 24
FONT_SIZE_GEAR  = 18
FONT_SIZE_LEAN  = 21
FONT_SIZE_META  = 13        
FONT_WEIGHT     = 'normal'  
STROKE_W        = 1.0       
STROKE_ALPHA    = 0.85

# ----------------------------
# Colors
# ----------------------------
DOT_COLOR      = 'red'
THROTTLE_COLOR = 'green'
BRAKE_COLOR    = 'red'

# Lean visuals
LEAN_RING_BG    = (0.75, 0.75, 0.75)   # grey outline arc
LEAN_FILL_COLOR = (1.00, 0.85, 0.15)   # default yellow
TEXT_COLOR      = 'black'

# Lean color thresholds (deg)
LEAN_LOW_DEG   = 25
LEAN_HIGH_DEG  = 50

LEAN_COLOR_LOW  = (1.0, 1.0, 1.0)      # white
LEAN_COLOR_MID  = (1.00, 0.85, 0.15)   # yellow
LEAN_COLOR_HIGH = (0.90, 0.20, 0.20)   # red
