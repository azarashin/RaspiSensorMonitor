import numpy as np
import matplotlib.pyplot as plt

import requests
import time
import json

class Graph:
    def __init__(self, device, attribs):
        self._xs = []
        self._yss = {d:[] for d in attribs}
        fig, ax = plt.subplots()
        self._fig = fig
        self._ax = ax
        self._start = None

    def update(self, records):
        tss = [d[0] for d in records]
        if len(tss) > 0 and self._start is None:
            self._start = tss[0]
        tss = [d - self._start for d in tss]
        self._ax.set_xlim([min(tss), max(tss)])
        lines = {}
        for record in records:
            vals = record[1]
            for attrib in vals:
                val = vals[attrib]
                if not attrib in lines:
                    lines[attrib] = []
                lines[attrib].append(val)
        #print(tss)
        #print(lines)
        plots = []
        for i, attrib in enumerate(vals): 
            plot, = self._ax.plot(tss, lines[attrib], color=f'C{i}', linestyle='-')
            plots.append(plot)

        self._ax.set_xlabel('X label')
        self._ax.set_ylabel('Y label')

        # 0.001秒停止
        plt.pause(0.001)
        for plot in plots:
            plot.remove()
    
class Viewer:
    def __init__(self, duration = 1.0):
        self._endpoint = 'http://192.168.0.21:8000/'
        res = requests.get(f'{self._endpoint}/attributes')
        res = requests.get(f'{self._endpoint}/current_timestamp')
        ts = json.loads(res.text)
        self._last_timestamp = ts['current_timestamp']
        self._duration = duration
        res = requests.get(f'{self._endpoint}/attributes')
        attributes = json.loads(res.text)
        devices = attributes.keys()
        self._log = {d:[] for d in devices}
        
        self._graphs = {d: Graph(d, attributes[d]) for d in attributes}

    def draw(self):
        for device in self._log:
            if device in self._graphs:
                graph = self._graphs[device]
                graph.update(self._log[device])
        
    def reload(self):
        res = requests.get(f'{self._endpoint}/logs?ts_begin={self._last_timestamp}')
        data = json.loads(res.text)
        last_timestamp = data['last_timestamp']
        logs = data['logs']
        head = float(last_timestamp) - self._duration
        #print(f'last_timestamp: {last_timestamp}, head: {head}')
        for device_name in logs:
            #print(f'device: {device_name}')
            records = logs[device_name]
            for record in records:
                ts = float(record['ts'])
                vals = record['vals']
                self._log[device_name].append((ts, vals))
                #print(f'ts: {ts}, vals: {vals}')
            self._log[device_name] = [d for d in self._log[device_name] if d[0] > head]
        self._last_timestamp = last_timestamp

v = Viewer(duration = 5.0)        
v.reload()
#v.draw()
for i in range(100):
    time.sleep(0.05)
    v.reload()
    v.draw()

