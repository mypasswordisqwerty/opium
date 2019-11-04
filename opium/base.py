from .app import AppData


class Base:
    def __init__(self):
        AppData().addObject(self)

    def update(self):
        pass
