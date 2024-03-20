import smbus
from time import sleep
from sensor_interface import SensorInterface

class ADXL345(SensorInterface):

    def __init__(self, address = 0x53, gForce=False):
        # select the correct i2c bus for this revision of Raspberry Pi
        self._revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
        self._bus = smbus.SMBus(1 if int(self._revision, 16) >= 4 else 0)

        # ADXL345 constants
        self.EARTH_GRAVITY_MS2   = 9.80665
        self.SCALE_MULTIPLIER    = 0.004

        self.DATA_FORMAT         = 0x31
        self.BW_RATE             = 0x2C
        self.POWER_CTL           = 0x2D

        self.BW_RATE_1600HZ      = 0x0F
        self.BW_RATE_800HZ       = 0x0E
        self.BW_RATE_400HZ       = 0x0D
        self.BW_RATE_200HZ       = 0x0C
        self.BW_RATE_100HZ       = 0x0B
        self.BW_RATE_50HZ        = 0x0A
        self.BW_RATE_25HZ        = 0x09

        self.RANGE_2G            = 0x00
        self.RANGE_4G            = 0x01
        self.RANGE_8G            = 0x02
        self.RANGE_16G           = 0x03

        self.MEASURE             = 0x08
        self.AXES_DATA           = 0x32

        self._gForce = gForce
        self._address = address
        self.set_bandwidth_rate(self.BW_RATE_100HZ)
        self.set_range(self.RANGE_2G)
        self.enable_measurement()

    def enable_measurement(self):
        self._bus.write_byte_data(self._address, self.POWER_CTL, self.MEASURE)

    def set_bandwidth_rate(self, rate_flag):
        self._bus.write_byte_data(self._address, self.BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def set_range(self, range_flag):
        value = self._bus.read_byte_data(self._address, self.DATA_FORMAT)

        value &= ~0x0F;
        value |= range_flag;
        value |= 0x08;

        self._bus.write_byte_data(self._address, self.DATA_FORMAT, value)

    def get_sensor_name(self):
        return 'ADXL345'

    def get_sensor_attributes(self):
        attrib = {"gForce": self._gForce}
        return attrib

    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def get_sensor_values(self):
        bytes = self._bus.read_i2c_block_data(self._address, self.AXES_DATA, 6)

        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * self.SCALE_MULTIPLIER
        y = y * self.SCALE_MULTIPLIER
        z = z * self.SCALE_MULTIPLIER

        if self._gForce == False:
            x = x * self.EARTH_GRAVITY_MS2
            y = y * self.EARTH_GRAVITY_MS2
            z = z * self.EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}

if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output
    # the current readings
    adxl345 = ADXL345()

    print(adxl345.get_sensor_attributes())
    while True:
      axes = adxl345.get_sensor_values()
      print(f"ADXL345 on address 0x{adxl345._address:x}: x = {axes['x']:.3f}G y = {axes['y']:.3f}G z = {axes['z']:.3f}")
      sleep(0.1)

