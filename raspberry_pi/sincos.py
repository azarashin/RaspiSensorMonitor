from time import sleep, time
import math
from sensor_interface import SensorInterface

class SinCos(SensorInterface):

    def __init__(self, freq = 5.0):
        self._freq= freq

    def get_sensor_name(self):
        return 'SinCos'

    def get_sensor_attributes(self):
        attrib = {}
        return attrib

    def get_sensor_values(self):
        t = time() * self._freq
        return {"sin": math.sin(t), "cos": math.cos(t)}

