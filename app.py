from flask import Flask
from flask_cors import CORS
import subprocess
import os
import platform
from pathlib import Path

app = Flask("ServerMon")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/heartbeat")
def heartbeat():
    return {"HeartBeat": True}

@app.route("/ssdtemp")
def ssd_temp():
    try:
        smartctl = Smartctl()
        devices = smartctl.devices
        if len(devices) > 0:
            for device in devices:
                # Assuming your SSD is the first device; modify as needed
                if device.temperature:
                    return {"Temp": f"{device.temperature}°C"}
                else:
                    return {"ERROR": "Temperature data not available for this SSD"}
        else:
            return {"ERROR": "No devices found"}
    except Exception as e:
        return {"ERROR": str(e)}

@app.route("/storage")
def storage():
    os_name = platform.system()

    if os_name == "Linux" or os_name == "Darwin":
        # For Linux/macOS
        out = subprocess.run(['df', '/', '--output=size,pcent'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        tot, percent = out.split("\n")[1].split()
        return {"Total": tot, "Percent": percent}

    elif os_name == "Windows":
        # For Windows
        result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        lines = output.splitlines()[1:]  # Skipping header row
        storage_info = []

        for line in lines:
            parts = line.split()
            if len(parts) == 3:
                caption, free_space, total_size = parts
                used_space = int(total_size) - int(free_space)
                percent_used = round((used_space / int(total_size)) * 100, 2)
                storage_info.append({
                    "Drive": caption,
                    "Total": total_size,
                    "Percent": f"{percent_used}%"
                })

        return {"Storage": storage_info}

    return {"ERROR": "Unsupported OS"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
