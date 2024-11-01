# ServerMon

A Flask-based API to monitor system resources, including CPU and storage usage and temperature and perform some admin actions.

## Features
- **Hello World**: Hello world :)
- **Heartbeat**: A simple API to check server status.
- **CPU Temperature**: Retrieves the CPU temperature using hardcoded cpu path.
- **Storage Usage**: Fetches total storage capacity and used percentage.
- **Storage Drive Temperature**: Uses `smartctl` (part of `smartmontools`) to retrieve drive temperature data.
- **Sleep**: Restart the server for `n` seconds.

## Running the server
1. Install docker, if it is not installed
* Ubuntu
    ```bash
    sudo apt install docker
    ```
* Arch
    ```bash
    sudo pacman -S docker
    ```

3. Download the latest docker image from the [releases page](https://github.com/SreeHarshan/ServerMonitor/releases/)

4. Load the docker image
    ```bash
    docker load -i <docker-file>
    ```

5. Run the docker image
    ```bash
    docker run --network host -p 8000:8000 -v /tmp:/tmp -v /home:/home <docker-image-name>
    ```

**Note**
- I have a cron script running that will log the temps of my ssd in `/tmp/sddtemp`, under the hood uses `smartmontools` which is used by api `ssdtemp`.
- The server runs on port 8000 and ip of 0.0.0.0, if you want to change the port or ip of server you can pass the port, ip as an env variable to docker by adding `docker run -e PORT=xxxx HOST=xxx.xxx.x.x ...`.
- I also have a cron script running that automatically restarts the server when the ssd temps reaches a threshold, writing a log into file at `/home/harshan/reachedtemp` which is being read by the api `/logs`.
- The cpu temps is being read at `/sys/class/thermal/thermal_zone6/temp` may vary from device to device.

## Build the docker file 

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/SreeHarshan/ServerMonitor.git
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
   
3. Install the requirements
    ```bash
    pip install -e requirements
    ```

4. Build the docker image 
    ```bash
    docker build -t <username>/<docker-image-name>:<version> .
    ```
5. Save the docker image to a file
   ```bash
   docker image save <image-name> -o <tar-file-name>
   ```

6. Perform steps from [Running the server](https://github.com/SreeHarshan/ServerMonitor/edit/main/README.md#running-the-server)

## Future Work
* Integrated the cronjob scripts into this repo
* Add api's to add .torrent file or magnet link to download a torrent.
* Fetch the progress of the torrent.
* Move the torrent to designated folder after complete.
