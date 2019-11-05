#!/usr/bin/env python3
import time
import sys
from opium import App, Led, Button, LedGroup, Config, Pin, Sensor
import datetime


class MyApp(App):
    CONF_TIME = 5
    FORE_TIME = 5*60
    BACK_TIME = 30

    def __init__(self):
        App.__init__(self)
        self.gate = Button(18).onChange(self.keyChange)
        self.door = Button(19).onChange(self.keyChange)
        self.fore = LedGroup([6], 1, Led(7))
        self.back = Led(13)
        self.light = LedGroup([1, 0, 3], Config().get('light'), Led(8))
        self.gateBtn = Button(9).onChange(self.onBtn)
        self.doorBtn = Button(10).onChange(self.onBtn).onLongPress(3, self.makeConf)
        self.backBtn = Button(20).onChange(self.addBack)
        self.lsens = Sensor(1005) if self.hasExpander() else None
        self.conftime = 0
        self.foretime = 0
        self.backtime = 0

    def makeConf(self, btn):
        self.light.on()
        time.sleep(0.5)
        self.light.off()
        time.sleep(0.5)
        self.light.on()
        self.conftime = self.CONF_TIME

    def keyChange(self, key):
        t = Config().get('time_end').split(':')
        te = datetime.time(int(t[0]), int(t[1])) if len(t) == 2 else None
        t = Config().get('time_start').split(':')
        ts = datetime.time(int(t[0]), int(t[1])) if len(t) == 2 else None
        lsensok = (self.lsens.value < Config().get('lsens')) if self.lsens else True
        while (ts or te) and lsensok:
            n = datetime.datetime.now().time()
            if ts and n > ts:
                break
            if te and n < te:
                break
            self.fore.setBlink(False)
            self.light.setBlink(False)
            return
        self.fore.setBlink(not self.gate.state)
        self.light.setBlink(not (self.gate.state and self.door.state))

    def foreSwitch(self):
        self.fore.switch()
        if self.fore.state:
            self.foretime = self.FORE_TIME

    def onBtn(self, btn):
        if not btn.state:
            return
        if btn == self.gateBtn:
            if not self.gate.state:
                self.fore.setBlink(not self.fore.blink)
            else:
                self.foreSwitch()
        if btn == self.doorBtn:
            if self.conftime > 0:
                c = self.light.conf+1
                if c > 7:
                    c = 1
                self.light.setConf(c)
                self.conftime = self.CONF_TIME
            else:
                self.light.switch()

    def addBack(self, btn):
        if btn and not btn.state:
            return
        self.backtime += self.BACK_TIME
        self.back.on()

    def processScgi(self, pack):
        if 'light' in pack:
            self.light.switch()
        if 'fore' in pack:
            self.foreSwitch()
        if 'conf' in pack:
            self.light.setConf(pack['conf'])
            Config().set('light', pack['conf']).save()
        if 'back' in pack:
            self.back.switch()
            self.backtime = 0
        if 'addback' in pack:
            self.addBack(None)
        ret = {'fore': self.fore.state, 'light': self.light.state,
               'conf': self.light.conf, 'door': self.door.state, 'gate': self.gate.state,
               'lsens': self.lsens.value if self.lsens else 'OFF',
               'back': self.back.state, 'backtime': int(self.backtime)
               }
        if "getconf" in pack:
            ret['time_start'] = Config().get('time_start')
            ret['time_end'] = Config().get('time_end')
        return ret

    def loop(self):
        if self.conftime > 0:
            self.conftime -= self.timeout
            if self.conftime <= 0:
                self.conftime = 0
                self.light.off()
                time.sleep(0.5)
                self.light.on()
                Config().set('light', self.light.conf).save()
        if self.foretime > 0:
            self.foretime -= self.timeout
            if self.foretime <= 0:
                self.foretime = 0
                self.fore.off()
        if self.backtime > 0:
            self.backtime -= self.timeout
            if self.backtime <= 0:
                self.backtime = 0
                self.back.off()


if __name__ == "__main__":
    sys.exit(MyApp().run())
