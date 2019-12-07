from .pin import Pin
from .app import AppData


class Gate(Pin):
    PRESS_TIME = 0.5
    PREOPEN_CL = 1

    def __init__(self, pin):
        Pin.__init__(self, pin, self.OUTPUT)
        self.timeout = AppData().timeout
        self.time = 0
        self._preopen = 0
        self._preopencl = 0
        self._ready = True

    def ready(self):
        return self._ready

    def preopen(self, time):
        self._preopen = time
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
                self._ready = (self.preopen == 0 and self.preopencl == 0)
        elif self._preopen > 0:
            self._preopen -= self.timeout
            if self._preopen <= 0:
                self._preopen = 0
                self._preopencl = self.PREOPEN_CL
                self.click()
        elif self._preopencl > 0:
            self._preopencl -= self.timeout
            if self._preopencl <= 0:
                self._preopencl = 0
                self.click()
        elif not self._ready:
            self.write(self.LOW)
            self._ready = True
