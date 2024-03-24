import time
import json



class Monitor:
  def __init__(self, sensors, capacity = 1000, interval_sec = 0.2):
    self._active = True
    self._sensors = sensors
    self._capacity = capacity
    self._interval_sec = interval_sec
    self._log = {d:[] for d in sensors}
    self._last_ts = time.time()

  def start(self):
    while self._active:
      time.sleep(self._interval_sec)
      ts = time.time()
      for sensor in self._sensors:
        self._log[sensor].append({'ts': ts, 'vals': sensor.get_sensor_values()})
        self._log[sensor] = self._log[sensor][-self._capacity:]
      self._last_ts = ts

  def stop(self):
    self._active = False
    time.sleep(1.0 + self._interval_sec)

  def get_attributes(self):
    attribs=[
        {'device': d.get_sensor_name(), 'attributes': d.get_sensor_attributes()}
        for d in self._sensors]
    return json.dumps(attribs)

  def get_device_list(self):
    devices=[d.get_sensor_name() for d in self._sensors]
    return json.dumps({'device_list': devices})

  def get_log(self, timestamp):
    logs=[{
        'device': d.get_sensor_name(),
        'records': [d0 for d0 in self._log[d] if d0['ts'] > timestamp]
        } for d in self._sensors]
    data = {'last_timestamp': self._last_ts, 'logs': logs}

    return json.dumps(data)

  def get_current_timestamp(self):
    return json.dumps({'current_timestamp': time.time()})
