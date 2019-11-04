from .gpio import GPIO
from .expander import Expander
from .singleton import Singleton
import time
from multiprocessing import Process, Pipe
from . import SCGIServer
from .config import Config


class AppData(metaclass=Singleton):
    DEF_TIMEOUT = 0.01
    CONF_RELOAD = 60*60*24

    def __init__(self):
        self.objs = []
        self.timeout = self.DEF_TIMEOUT
        self.conf_reload = self.CONF_RELOAD

    def addObject(self, obj):
        self.objs += [obj]


class App:

    def __init__(self):
        GPIO()
        self.timeout = AppData().timeout
        self.expander = None
        if Config().get('expander'):
            self.expander = Expander()
            GPIO().setExpander(self.expander)

    def hasExpander(self):
        return self.expander != None

    def loop(self):
        pass

    def processScgi(self, pack):
        return True

    def run(self):
        port = Config().get('scgi_port', 4000)
        if port != 0:
            self.pipe, rempipe = Pipe()
            proc = Process(target=SCGIServer.serve, args=(rempipe, port))
            proc.daemon = True
            proc.start()
        conf_reload = AppData().conf_reload
        while True:
            for x in AppData().objs:
                x.update()
            self.loop()
            if port != 0 and self.pipe.poll():
                obj = self.pipe.recv()
                ret = self.processScgi(obj)
                self.pipe.send(ret)
            conf_reload -= self.timeout
            if conf_reload <= 0:
                Config().reload()
                conf_reload = AppData().conf_reload
            time.sleep(self.timeout)
        self.pipe.close()
