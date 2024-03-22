import sys
import threading
import time
from flask import Flask, request

from monitor import Monitor

from ADXL345 import ADXL345
from MCP3008 import MCP3008
from sincos import SinCos

#ip=input('ip address:')
#port=input('port:')

if len(sys.argv) != 3:
    print('usage: python3 server.py {ip address} {port number}')
    exit()

ip=sys.argv[1]
port=int(sys.argv[2])

monitor = Monitor([
    ADXL345(),
    MCP3008(),
    SinCos(),
    ], capacity=1000, interval_sec=0.02)

app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/logs')
def logs():
    req = request.args
    ts_begin = req.get("ts_begin")
    if ts_begin is None:
        ts_begin = 0
    else:
        try:
            ts_begin = float(ts_begin)
        except ValueError:
            ts_begin = 0
    return monitor.get_log(ts_begin)

@app.route('/attributes')
def attributes():
    return monitor.get_attributes()

@app.route('/current_timestamp')
def current_timestamp():
    return monitor.get_current_timestamp()

@app.route('/device_list')
def device_list():
    return monitor.get_device_list()


def start_monitor():
    monitor.start()

thread = threading.Thread(target=start_monitor)
thread.start()

try:
    app.run(host=ip, port=port, debug=True)
finally:
    monitor.stop()
    thread.join()

