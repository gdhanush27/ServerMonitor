from flask import Flask,request
from flask_cors import CORS, cross_origin
import subprocess
import os
import platform
from pathlib import Path

app = Flask("ServerMon")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route("/cputemp")
def cpu_temp():
    out = subprocess.run(['cat','/sys/class/thermal/thermal_zone6/temp'],stdout=subprocess.PIPE).stdout.decode('utf-8')
    return {"Temp":out}

@app.route("/storage")
def storage():
    out = subprocess.run(['df', '/', '--output=size,pcent'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    tot, percent = out.split("\n")[1].split()
    return {"Total": tot, "Percent": percent}
    
@app.route("/addtorrent")
def addtorrent():
    pass

@app.route("/sleep")
def sleep():
    time = request.args.get('time')
    out = os.system("rtcwake -m off -s {}".format(time))
    return {"Output":"Success" if out == 0 else "Failed"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
