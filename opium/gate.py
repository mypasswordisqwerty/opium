from .pin import Pin


class Gate(Pin):
    PRESS_TIME = 0.5

    def __init__(self, pin):
        Pin.__init__(self, pin, self.OUTPUT)
        self.timeout = AppData().timeout
        self.time = 0

    def click(self):
        self.time = self.PRESS_TIME
        self.write(self.HIGH)

    def update(self):
        if self.time > 0:
            self.time -= self.timeout
            if self.time <= 0:
                self.time = 0
                self.write(self.LOW)
