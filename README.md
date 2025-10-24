# MotoGP 18 Telemetry Dashboard

A data visualization tool for the MotoGP 18 video game.

**STATUS:** WIP

## Data Source

Telemetry CSVs were exported from *MotoGP 18* using the [Sim Racing Telemetry](https://store.steampowered.com/app/845210/Sim_Racing_Telemetry/) tool on Steam

## Demo
<video src="assets/demo.mp4" width="800" autoplay loop muted playsinline>
</video>

[demo](https://github.com/Denn-LC/MotoGP18-Telemetry/raw/main/assets/demo.mp4)

## Requirements
- Python 3.13.5
- Install dependencies:

```bash
pip install -r requirements.txt
```

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