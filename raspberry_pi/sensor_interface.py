from abc import ABCMeta, abstractmethod

class SensorInterface(object, metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def get_sensor_name(self):
        return 'dummy'

    @abstractmethod
    def get_sensor_values(self):
        values = [
            {'attribute': 'valueA', 'value': 10},
            {'attribute': 'valueB', 'value': 20},
        ]
        return values

    @abstractmethod
    def get_sensor_attributes(self):
        attributes = [
            {'name': 'attributeA', 'value': 'abc' },
            {'name': 'attributeB', 'value': 'xyz' }
        ]

        return attributes

