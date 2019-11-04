from led import Led
from base import Base
from app import AppData


class LedGroup(Base):
    BLINK_TIME = 0.5

    def __init__(self, pins, conf, indicator):
        Base.__init__(self)
        self.leds = []
        self.ind = indicator
        for x in pins:
            self.leds += [Led(x)]
        self.state = False
        self.blink = False
        self.btime = 0
        self.timeout = AppData().timeout
        self.setConf(conf)

    def setConf(self, conf):
        self.conf = conf
        self.setState(self.state)

    def setState(self, state):
        self.state = state
        self.ind.setState(not state)
        c = self.conf
        for x in self.leds:
            x.setState((state or self.blink) and (c & 1))
            c >>= 1

    def setBlink(self, blink):
        self.blink = blink
        self.setState(self.state)

    def on(self): self.setState(True)

    def off(self): self.setState(False)

    def switch(self): self.setState(not self.state)

    def update(self):
        if self.blink and not self.state:
            self.btime -= self.timeout
            if self.btime < 0:
                self.btime = self.BLINK_TIME
                self.ind.switch()
