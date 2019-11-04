from .pin import Pin
from .app import AppData


class Button(Pin):
    DEBOUNCE_TIME = 0.025

    def __init__(self, pin, initial=False):
        Pin.__init__(self, pin, self.INPUT, self.PULLUP)
        self.state = 0
        self.dbounce = 0
        self.changeProc = None
        self.longPress = []
        self.pressTime = 0
        self.timeout = AppData().timeout

    def onChange(self, proc):
        self.changeProc = proc
        return self

    def onLongPress(self, duration, proc):
        self.longPress += [{'proc': proc, 'dur': duration, 'time': 0}]
        return self

    def update(self):
        s = self.read()
        s = not s
        if self.dbounce > 0:
            self.dbounce -= self.timeout
        if s == self.state:
            if not s:
                return
            for x in self.longPress:
                if x['time'] < 0:
                    continue
                x['time'] -= self.timeout
                if x['time'] < 0:
                    x['proc'](self)
            return
        if self.dbounce > 0:
            return
        self.state = s
        if s and self.longPress:
            for x in self.longPress:
                x['time'] = x['dur']
        self.dbounce = self.DEBOUNCE_TIME
        if self.changeProc:
            self.changeProc(self)
