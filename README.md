# MotoGP 18 Telemetry Dashboard

A data visualization tool for the MotoGP 18 video game

## Demo
[Watch the tool in action](https://github.com/user-attachments/assets/3388a4b9-a0f4-46b8-92e6-c87c4a30ec31)

## Features
- Real time animated telemetry playback
- Live HUD with lean angle, throttle and brake visualizations
- Lap timer with gear and speed readings
- Drawn 2D track map with a start and finish line
- Smoothed signal processing for realistic telemetry behavior

## Technical Overview
- Built with **Python 3.13.5**, using `pandas`. `matplotlib`, and `numpy`
- Modulated for clarity
  - `data_load.py`: reads, cleans and processes raw telemetry
  - `graphics.py`: draws the HUD, track map and other visualizations
  - `animation.py`: handles real time updates and visuals
  - `utils.py`: small helper functions including smoothing and formatting
  - `config.py`: all constants and tunable parameters formatted nicely for fast tuning

## How to run
To run the dashboard locally:

1. Clone this repo:
```bash
git clone https://github.com/Denn-LC/motogp18-telemetry.git
cd motogp18-telemetry
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. From the root project folder (motogp_dashboard/) run:
```bash
python -m motogp_dashboard.main
```
(The example telemetry file 'new_example.csv' is automatically loaded)

## Credits and Acknowledgements
Developed by Dennison Leadbetter-Clarke
Telemetry CSVs were exported from *MotoGP 18* using the [Sim Racing Telemetry](https://store.steampowered.com/app/845210/Sim_Racing_Telemetry/) tool on Steam
Project created for portfolio demonstration purposes

This project also benefit from feedback and testing from a few university peers, whose input helped refine the project, thank you!

## Version
**v1.0 Final release**

This version represents the completed showcase build of the project
Additional features such as adjustable playback speed or expanded telemetry overlays may be added in future updates
