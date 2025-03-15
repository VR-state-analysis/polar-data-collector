# Polar Data Collector

A quick script to collect data from a Polar H9, and save all data to an SQLite database (`polar_data_collector.db`).

## Running

### This Software

- Navigate to this directory
- `python3 -m venv venv` to create a virtual environment (location does not matter)
- `venv/bin/pip install -r requirements.txt` to install the required packages
- `venv/bin/python3 polar_data_collector` to run the script

### Lower-level Software and Hardware

Tested on a Raspberry Pi 4B running Raspberry Pi OS (64-bit).
No special modifications were done to the Raspberry Pi BIOS or OS (bluez was already installed).
