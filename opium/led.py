from pin import Pin


class Led(Pin):
    def __init__(self, pin, initial=False):
        Pin.__init__(self, pin, self.OUTPUT)
        self.setState(initial)

    def setState(self, state):
        self.state = state
        self.write(self.HIGH if self.state else self.LOW)

    def getState(self):
        return self.state

    def on(self):
        self.setState(True)

    def off(self):
        self.setState(False)

    def switch(self):
        self.setState(not self.state)
