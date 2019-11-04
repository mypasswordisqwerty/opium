try:
    from pyA20.i2c import i2c
    from pyA20.gpio import gpio
except:
    i2c = None


GPIO_EXPANDER_RESET = 0x01
GPIO_EXPANDER_PORT_MODE_INPUT = 0x04
GPIO_EXPANDER_PORT_MODE_PULLUP = 0x05
GPIO_EXPANDER_PORT_MODE_PULLDOWN = 0x06
GPIO_EXPANDER_PORT_MODE_OUTPUT = 0x07
GPIO_EXPANDER_DIGITAL_READ = 0x08
GPIO_EXPANDER_DIGITAL_WRITE_HIGH = 0x09
GPIO_EXPANDER_DIGITAL_WRITE_LOW = 0x0A
GPIO_EXPANDER_ANALOG_WRITE = 0x0B
GPIO_EXPANDER_ANALOG_READ = 0x0C


class Expander:

    def __init__(self, dev="/dev/i2c-0", addr=0x2A, expin=1000):
        self.expin = expin
        self.addr = addr
        if not i2c:
            return
        i2c.init(dev)
        i2c.open(self.addr)

    def __del__(self):
        i2c.close()

    def writeCmd(self, cmd, data16=None):
        data = [cmd]
        if data16 is not None:
            data += [data16 >> 8, data16 & 0xFF]
        i2c.write(data)

    def read16(self, cmd):
        self.writeCmd(cmd)
        data = i2c.read(2)
        return data[0] << 8 | data[1]

    def mkpin(self, pin):
        return 1 << (pin - self.expin)

    def setcfg(self, pin, mode):
        cmd = GPIO_EXPANDER_PORT_MODE_OUTPUT if mode == gpio.OUTPUT else GPIO_EXPANDER_PORT_MODE_INPUT
        self.writeCmd(cmd, self.mkpin(pin))

    def pullup(self, pin, mode):
        cmd = GPIO_EXPANDER_PORT_MODE_PULLUP if mode == gpio.PULLUP else GPIO_EXPANDER_PORT_MODE_PULLDOWN
        self.writeCmd(cmd, self.mkpin(pin))

    def dread(self, pin):
        data = self.read16(GPIO_EXPANDER_DIGITAL_READ)
        return (data & self.mkpin(pin)) != 0

    def dwrite(self, pin, val):
        if val:
            self.writeCmd(GPIO_EXPANDER_DIGITAL_WRITE_HIGH, self.mkpin(pin))
        else:
            self.writeCmd(GPIO_EXPANDER_DIGITAL_WRITE_LOW, self.mkpin(pin))

    def aread(self, pin):
        i2c.write([GPIO_EXPANDER_ANALOG_READ, pin-self.expin])
        data = i2c.read(2)
        return data[0] << 8 | data[1]

    def awrite(self, pin, val):
        data = [GPIO_EXPANDER_ANALOG_WRITE, pin-self.expin, val, val]
        i2c.write(data)
