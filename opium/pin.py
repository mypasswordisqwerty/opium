from .gpio import GPIO
from .app import AppData
from .base import Base


class Pin(Base):
    PULLUP = 1
    PULLDOWN = 2
    INPUT = 0
    OUTPUT = 1
    HIGH = 1
    LOW = 0

    def __init__(self, pin, mode, pullup=None):
        Base.__init__(self)
        self.pin = pin
        GPIO().setcfg(pin, mode)
        if pullup:
            GPIO().pullup(pin, pullup)

    def read(self):
        return GPIO().input(self.pin)

    def write(self, val):
        GPIO().output(self.pin, val)

    def aread(self):
        return GPIO().aInput(self.pin)

    def awrite(self, val):
        GPIO().aOutput(self.pin, val)
