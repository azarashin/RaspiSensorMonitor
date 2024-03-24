import spidev
from time import sleep
from sensor_interface import SensorInterface

class MCP3008(SensorInterface):

    def __init__(self, max_speed_hz = 100000, mode = 0x03, mask=0x01):
        self._max_speed_hz = max_speed_hz
        self._mode = mode
        self._mask = mask

        spi = spidev.SpiDev()
        spi.close()
        spi.open(0,0)
        spi.max_speed_hz = self._max_speed_hz
        spi.mode = self._mode

        self._spi = spi

    def analog_read(self, channel):
        r = self._spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((r[1]&3) << 8) + r[2]
        return adc_out

    def get_sensor_name(self):
        return 'MCP3008'

    def get_sensor_attributes(self):
        attrib = [
            {'name': 'max_speed_hz', 'value': self._max_speed_hz},
            {'name': 'mode', 'value': self._mode},
        ]
        return attrib

    def get_sensor_values(self):
        reading = [
            {'attribute': f'ch{d}', 'value': self.analog_read(d) / 1023.0}
        for d in range(0, 8) if (1 << d) & self._mask != 0]
        return reading

if __name__ == "__main__":
    mcp3008 = MCP3008()

    print(mcp3008.get_sensor_attributes())
    while True:
      values = mcp3008.get_sensor_values()
      print(values)
      sleep(0.1)

