from abc import ABCMeta, abstractmethod

class SensorInterface(object, metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def get_sensor_name(self):
        return 'dummy'

    @abstractmethod
    def get_sensor_values(self):
       values = {'valueA': 10, 'valueB': 20}
       return values

    @abstractmethod
    def get_sensor_attributes(self):
       attributes = {'attributeA': 'abc', 'attributeB': 'xyz'}
       return attributes

