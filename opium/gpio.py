from singleton import Singleton
import logging
try:
    from pyA20.gpio import gpio as G
    EMU = False
except:
    EMU = True


class GPIO:
    __metaclass__ = Singleton

    def __init__(self):
        self.expander = None
        self.expin = 999
        if EMU:
            self.state = {}
            print "gpio emulator enabled"
        else:
            G.init()

    def setExpander(self, exp):
        self.expander = exp
        self.expin = exp.expin-1

    def setcfg(self, pin, mode):
        if EMU:
            print "PIN", pin, ": mode", mode
            self.state[pin] = {'mode': mode, 'val': 0}
            return
        if pin > self.expin:
            self.expander.setcfg(pin, mode)
        G.setcfg(pin, mode)

    def pullup(self, pin, mode):
        if EMU:
            print "PIN", pin, ": pullup", mode
            return
        if pin > self.expin:
            self.expander.pullup(pin, mode)
            return
        G.pullup(pin, mode)

    def input(self, pin):
        if EMU:
            res = self.state[pin]['val']
            return res
        if pin > self.expin:
            return self.expander.dread(pin)
        return G.input(pin)

    def output(self, pin, val):
        if EMU:
            print "PIN", pin, ": write", val
            self.state[pin]['val'] = val
            return
        if pin > self.expin:
            return self.expander.dwrite(pin, val)
        return G.output(pin, val)

    def aInput(self, pin):
        if EMU:
            res = self.state[pin]['val']
            return res
        if pin > self.expin:
            return self.expander.aread(pin)
        return G.input(pin)

    def aOutput(self, pin, val):
        if EMU:
            print "PIN", pin, ": write", val
            self.state[pin]['val'] = val
            return
        if pin > self.expin:
            return self.expander.awrite(pin, val)
        return G.output(pin, val)
