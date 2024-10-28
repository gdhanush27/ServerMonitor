# ServerMon

A Flask-based API to monitor system resources, including CPU and storage usage and temperature, across multiple operating systems (`Linux`, `macOS`, and `Windows`).

## Features
- **Heartbeat**: A simple API to check server status.
- **CPU Temperature**: Retrieves the CPU temperature using `sensors` on Linux or `WMIC` on Windows.
- **Storage Usage**: Fetches total storage capacity and used percentage.
- **Storage Drive Temperature**: Uses `smartctl` (part of `smartmontools`) to retrieve drive temperature data.

## Prerequisites
Ensure you have the following installed:
- **Python 3.x**
- **Flask** and **Flask-CORS** Python libraries
- **smartmontools**:
  - **Linux**: Needed for storage temperature monitoring.
  - **Windows**: Ensure `smartctl` is accessible in your `PATH`.

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. **Clone the Repository**:

```bash
git clone https://github.com/gdhanush27/ServerMonitor.git
cd ServerMon
```
2. **Install smartmontools**:

    - *For Arch Linux*:

    ```bash

    sudo pacman -S smartmontools
    ```
    - *For Debian/Ubuntu*:

    ```bash

    sudo apt update && sudo apt install smartmontools
    ```
    - *For Windows*:
        - Download smartmontools from https://www.smartmontools.org/.
        - Add the smartctl.exe binary to your system PATH.

## Run the Application:

```bash
python app.py
```
The server will start at http://0.0.0.0:5000 by default.

## API Endpoints

1. **Heartbeat**
    - Endpoint: `/heartbeat`
    - Method: `GET`
    - Description: Returns a simple heartbeat JSON to check if the server is running.

2. **CPU Temperature**
    - Endpoint: `/cputemp`
    - Method: `GET`
    - Description: Retrieves the CPU temperature.
    - OS Support: Linux (requires `sensors`), Windows (uses `WMIC`).

3. **Storage Usage**
    - Endpoint: `/storage`
    - Method: `GET`
    - Description: Provides total storage capacity and usage percentage.
    - OS Support: Linux/macOS (uses `df`), Windows (uses `WMIC`).

4. **Storage Drive Temperature** ( *Yet to be released* )
    - Endpoint: `/storagetemp`
    - Method: `GET`
    - Description: Retrieves the temperature of each storage drive using smartctl.
    - OS Support: Linux, Windows (both require `smartmontools`).

## Notes

- The `storagetemp` endpoint requires `smartmontools`, which may need root privileges to access drive data.
- The `cputemp` endpoint on Linux depends on `sensors`, which can be installed with `sudo pacman -S lm_sensors` on Arch or `sudo apt install lm-sensors` on Debian/Ubuntu. `Run sudo sensors-detect` to configure.