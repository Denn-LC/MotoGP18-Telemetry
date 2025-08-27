import os

# File paths
DATA_DIR = 'data'
FILENAME = "new_example.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)

# cleaning parameters
INTERPOLATE_LIMIT = 10  # only takes small gaps
JUMP_SIGMA = 5  # GPS jump cutoff = mean + JUMP_SIGMA * std

# timing
DT_PER_TICK = 0.01  # as binIndex is 100Hz
MIN_DT = 0.01  # avoid any freezes on 0
MAX_DT = 0.2  # avoid spikes

# overlay visuals
TRACK_SIZE = (6, 6)  # size of the track
TRACK_UNDERLAY = True
TRACK_COLOR = (0.20, 0.20, 0.20)  # grey
TRACK_ALPHA = 0.25
TRACK_LINEWIDTH = 1.2


THROTTLE_BAR_POSITION = [0.76, 0.55, 0.06, 0.35]
BRAKE_BAR_POSITION = [0.90, 0.55, 0.06, 0.35]

GEAR_POS = (0.02, 0.3)
RPM_POS = (0.02, 0.89)
THROTTLE_TXT_POS = (0.02, 0.83)
BRAKE_TXT_POS = (0.02, 0.77)
SPEED_TXT_POS = (0.02, 0.71)
LAP_TXT_POS   = (0.02, 0.65)

TRAIL_LEN = 60 

# colors
DOT_COLOR = 'red'
TRACK_COLOR = 'black'
TRAIL_COLOR = '#8000FF'
THROTTLE_COLOR = 'green'
BRAKE_COLOR = 'red'
RPM_COLOR = 'blue'
GEAR_COLOR = 'orange'