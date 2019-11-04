from .singleton import Singleton
import os
import json


class Config(metaclass=Singleton):

    def __init__(self):
        self.file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.json"))
        self.reload()

    def reload(self):
        with open(self.file) as f:
            self.conf = json.load(f)

    def get(self, name, default=None):
        if name not in self.conf:
            return default
        return self.conf[name]

    def set(self, name, val):
        self.conf[name] = val
        return self

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.conf, f, indent=4)
