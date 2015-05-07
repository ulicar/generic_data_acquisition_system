__author__ = 'jdomsic'


class SensorNode(object):
    def __init__(self, app_id, unique_id, module_type, value, timestamp, optional=()):
        self.app_id = app_id
        self.id = unique_id
        self.module = module_type
        self.value = value
        self.timestamp = timestamp
        self.optional = optional

    def validate(self):
        assert type(self.id) is str and self.id != ''
        assert type(self.timestamp) is int
        assert self.module is not None
        assert self.value is not None

    def get(self):
        return self.__dict__

    def update_value(self, timestamp, value):
        self.value = value
        self.timestamp = timestamp

if __name__ == '__main__':
    import json
    import time

    DUMMY = 0
    sensor = SensorNode('Temperature sensor', 'zxy44', 'temperature', DUMMY, DUMMY)
    sensor.validate()

    while True:
        TIME = int(time.time())

        sensor.update_value(timestamp=TIME, value=TIME % 50)

        print json.dumps(sensor.get())
        time.sleep(0.99)
