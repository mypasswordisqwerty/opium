from .pin import Pin
from .app import AppData


class Gate(Pin):
    PRESS_TIME = 0.5

    def __init__(self, pin):
        Pin.__init__(self, pin, self.OUTPUT)
        self.timeout = AppData().timeout
        self.time = 0
        self.clicks = []
        self._ready = True

    def ready(self):
        return self._ready

    def preopen(self, time):
        self.clicks = [time, 1, 1]
        self.click()

    def click(self):
        self.time = self.PRESS_TIME
        self._ready = False
        self.write(self.HIGH)

    def update(self):
        if self.time > 0:
            self.time -= self.timeout
            if self.time <= 0:
                self.time = 0
                self.write(self.LOW)
                self._ready = len(self.clicks) == 0
        elif len(self.clicks) > 0:
            self.clicks[0] -= self.timeout
            if self.clicks[0] <= 0:
                self.clicks = self.clicks[1:]
                self.click()
        elif not self._ready:
            self.write(self.LOW)
            self._ready = True
