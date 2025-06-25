# MotoGP 18 Telemetry Dashboard (videogame)

This is a python based telemetry analysis tool that uses exported data from MotoGP18 videogame to simulate real data, the SRT (Sim Racing Technology) plugin on steam was used in order to export the data from the videogame.

# Goal features
- load and process CSV telemetry files from SRT
- Plot:
    - Speed vs Time
    - Throttle/Break vs Time
    - Gear and RPM
    - Lean angle (if avaliable)
    - Possibly a 2D race map using X and Y position data

# Requirements
- Python 3.8+
- Install dependencies:
```bash
pip install pandas matplotlib numpy