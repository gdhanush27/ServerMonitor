from flask import Flask
from flask_cors import CORS, cross_origin
import subprocess
import os
from pathlib import Path

app = Flask("ServerMon")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/heartbeat")
def heartbeat():
    return {"HeartBeat":True}

@app.route("/ssdtemp")
def ssd_temp():

    cwd = os.getcwd()
    file = "/tmp/ssd_temp"
    relpath = os.path.relpath(file,cwd)

    if(not os.path.exists(relpath)):
        print(relpath)
        return {"ERROR":"Path does not exist"}
    with open(relpath) as f: 
        val = f.readline()[:-1]
        f.close()

    return {"Temp":val}

@app.route("/storage")
def storage():
    out = subprocess.run(['df','/','--output=size,pcent'],stdout=subprocess.PIPE).stdout.decode('utf-8')

    tot,percent = out.split("\n")[1].split()

    return {"Total":tot,"Percent":percent}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))