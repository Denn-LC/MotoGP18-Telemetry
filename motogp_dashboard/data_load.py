import pandas as pd
import numpy as np

from motogp_dashboard import config

def load_data():
    try:
        df = pd.read_csv(config.CSV_PATH, sep="\t")
        print(f"Loaded {len(df)} rows from '{config.FILENAME}'")

        # Drop any laps when lap is 0
        if 'lapIndex' in df.columns:
            race_rows = df['lapIndex'] > 0
            df = df[race_rows].reset_index(drop = True)

        # Throttle
        df['throttle'] = df['throttle'].replace(-1.0, np.nan)
        df['throttle'] = df['throttle'].interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')
        df['throttle'] = df['throttle'].clip(lower = 0, upper = 1)

        # Brake
        df['brake_0'] = df['brake_0'].replace(-1.0, np.nan)
        df['brake_0'] = df['brake_0'].interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')
        df['brake_0'] = df['brake_0'].clip(lower = 0, upper = 1)

        # RPM
        df['rpm'] = df['rpm'].replace(-1.0, np.nan)
        df['rpm'] = df['rpm'].interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')
        df['rpm'] = df['rpm'].clip(lower = 0)

        # Gear
        df['gear'] = df['gear'].replace(-1, np.nan)
        df['gear'] = df['gear'].ffill().bfill()
        df['gear'] = df['gear'].round().clip(lower = 1, upper = 6)
        df['gear'] = df['gear'].astype(int)

        # Positions
        df['world_position_X'] = df['world_position_X'].replace(-1.0, np.nan)
        df['world_position_X'] = df['world_position_X'].interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')
        df['world_position_Y'] = df['world_position_Y'].replace(-1.0, np.nan)
        df['world_position_Y'] = df['world_position_Y'].interpolate(limit = config.INTERPOLATE_LIMIT, limit_direction = 'both')

        # Drop rows with NaNs
        df = df.dropna(subset = [
            'world_position_X', 'world_position_Y',
            'throttle', 'brake_0', 'rpm', 'gear'
        ]).reset_index(drop = True)

        # Remove GPS jumps
        dx = df['world_position_X'].diff()
        dy = df['world_position_Y'].diff()
        distance = (dx**2 + dy**2) ** 0.5
        jump_threshold = distance.mean() + config.JUMP_SIGMA * distance.std()
        valid_rows = distance.fillna(0) < jump_threshold
        df = df[valid_rows].copy().reset_index(drop = True)

        # Timing
        bin_index_diff = df['binIndex'].diff()
        df['dt_raw'] = (bin_index_diff.fillna(1) * config.DT_PER_TICK).clip(lower = 0)
        df['dt'] = df['dt_raw'].clip(lower = config.MIN_DT, upper = config.MAX_DT)
        df['time_s'] = df['dt_raw'].cumsum()

        # Speed
        vx = df['velocity_X']
        vy = df['velocity_Y']
        vz = df['velocity_Z']
        df['speed_mps'] = np.sqrt(vx**2 + vy**2 + vz**2)
        df['speed_kph'] = df['speed_mps'] * 3.6

        return df

    except Exception as e:
        print(f"Failed to load or clean CSV: {e}")
        return None
if __name__ == "__main__":
    main()
