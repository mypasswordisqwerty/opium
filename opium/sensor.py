from .pin import Pin


class Sensor(Pin):
    def __init__(self, pin):
        Pin.__init__(self, pin, self.INPUT)
        self.value = None

    def update(self):
        self.value = self.aread()
