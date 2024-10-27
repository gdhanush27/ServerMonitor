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
    cwd = os.getcwd()
    file = "/tmp/ssd_temp"
    relpath = os.path.relpath(file, cwd)

    if not os.path.exists(relpath):
        print(relpath)
        return {"ERROR": "Path does not exist"}
    
    with open(relpath) as f:
        val = f.readline()[:-1]
    
    return {"Temp": val}

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

@app.route("/cputemp")
def cpu_temp():
    os_name = platform.system()

    if os_name == "Linux":
        try:
            # Try to get CPU temperature using `sensors` command
            result = subprocess.run(['sensors'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            for line in output.splitlines():
                if "Package id 0" in line or "Tdie" in line:  # Adjust according to your CPU (AMD/Intel)
                    temp = line.split()[3]  # Extract temperature value
                    return {"CPU_Temp": f"{temp[1:]}"}
            return {"ERROR": "Temperature data not found"}
        except Exception as e:
            return {"ERROR": str(e)}

    elif os_name == "Windows":
        try:
            # Use WMIC to get CPU temperature
            result = subprocess.run(
                ['wmic', 'path', 'Win32_PerfFormattedData_Counters_ThermalZoneInformation', 'get', 'Temperature'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            output = result.stdout
            temperatures = None
            for line in output.splitlines()[1:]:  # Skip header
                if line.strip():  # If line is not empty
                    temp_kelvin = int(line.strip())
                    temp_celsius =temp_kelvin - 273.15  # Convert from tenths of Kelvin to Celsius
                    temperatures = f"{temp_celsius:.2f}°C"
            if temperatures:
                return {"CPU_Temps": temperatures}
            return {"ERROR": "Temperature data not found"}
        except Exception as e:
            return {"ERROR": str(e)}

    return {"ERROR": "Unsupported OS"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
