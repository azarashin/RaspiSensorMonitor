import matplotlib.pyplot as plt
import sys
import requests
import time
import json
import threading
import matplotlib.style as mplstyle
class Graph:
    def __init__(self, duration, delay):
#        self._xs = []
#        self._yss = {d:[] for d in attribs}
        fig, ax = plt.subplots()
        self._fig = fig
        self._ax = ax
        self._start = None
        self._actual_start = None
        self._duration = duration - delay
        self._delay = delay

    def update(self, records):
        tss = [d[0] for d in records]
        if len(tss) > 0 and self._start is None:
            self._start = tss[0]
            self._actual_start = time.time()
        start_acutial_time_to_show = time.time() - self._actual_start - self._duration - self._delay
        end_acutial_time_to_show = time.time() - self._actual_start - self._delay
        start_ts_to_show = start_acutial_time_to_show + self._start
        end_ts_to_show = end_acutial_time_to_show + self._start
        records = [d for d in records if d[0] > start_ts_to_show and d[0] <= end_ts_to_show]
        tss = [d[0] for d in records]

        tss = [d - self._start for d in tss]
        if len(tss) == 0:
            return
        self._ax.set_xlim([min(tss), max(tss)])
        #print('A', time.time(), start_ts_to_show, end_ts_to_show, max(tss), min(tss), max(tss) - min(tss))
        lines = {}
        for record in records:
            vals = record[1]
            for attrib in vals:
                attrib_name = attrib['attribute']
                val = attrib['value']
                if not attrib_name in lines:
                    lines[attrib_name] = []
                lines[attrib_name].append(val)
        #print(tss)
        #print(lines)
        plots = []
        for i, attrib in enumerate(vals): 
            attrib_name = attrib['attribute']
            plot, = self._ax.plot(tss, lines[attrib_name], color=f'C{i}', linestyle='-')
            plots.append(plot)

        self._ax.set_xlabel('X label')
        self._ax.set_ylabel('Y label')

        # 0.001秒停止
        plt.pause(0.001)
#        for plot in plots:
#            plot.remove()
    
class Viewer:
    def __init__(self, ipHost, port, buffer_duration = 15.0, view_duration = 5.0, delay = 1.0):
        self._endpoint = f'http://{ipHost}:{port}/'
        res = requests.get(f'{self._endpoint}/current_timestamp')
        ts = json.loads(res.text)
        self._last_timestamp = ts['current_timestamp']
        self._duration = buffer_duration
        self._delay = delay
        res = requests.get(f'{self._endpoint}/attributes')
        attributes = json.loads(res.text)
        devices = [d['device'] for d in attributes]
        self._log = {d:[] for d in devices}
        
        self._graphs = {d: Graph(view_duration, delay) for d in devices}

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
        head = float(last_timestamp) - self._duration - self._delay
        #print(f'last_timestamp: {last_timestamp}, head: {head}')
        for log in logs:
            device = log['device']
            records = log['records']
            #print(f'device: {device}')
            for record in records:
                ts = float(record['ts'])
                vals = record['vals']
                self._log[device].append((ts, vals))
                #print(f'ts: {ts}, vals: {vals}')
            self._log[device] = [d for d in self._log[device] if d[0] > head]
        self._last_timestamp = last_timestamp

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python .py ipHost port')
        exit()
    ipHost = sys.argv[1]
    port = sys.argv[2]
    mplstyle.use('fast')

    v = Viewer(ipHost, port, buffer_duration = 15.0, view_duration = 5.0, delay=3.0)        
    v.reload()
    running = True

    def thread_network():
        while running:
            # Burst transmission
            v.reload()
            time.sleep(2)


    thread_network_task = threading.Thread(target=thread_network, name='network', daemon=True)
    thread_network_task.start()

    while running:
        time.sleep(0.05)
        v.draw()

    try:
        while running:
            time.sleep(0.05)
            v.draw()
    except:
        running = False

    thread_network_task.join()
