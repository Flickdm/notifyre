import logging
import weakref

from .LedStrip import ILedStrip
from .OutputDevice import IOutputDevice

logger = logging.getLogger(__name__)

class CachedHardwareManager(object):
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_hardware(self, name):
        if name not in self._cache:
            hw = HardwareFactory(name)
            self._cache[name] = hw
        else:
            hw = self._cache[name]

        return hw

    def clear(self):
        self._cache.clear()

class HardwareFactory(object):
    manager = CachedHardwareManager()

    def __init__(self, name):
        self.name = name
        self.output_devices = {}
        self.led_strips = {}

    def create_output_device(self, name="pwr", pin=25):
        if name not in self.output_devices:
            self.output_devices[name] = IOutputDevice(pin)

    def create_led_strip(self, name="leds", pins=[18, 23, 24]):

        if len(pins) != 3:
            raise ValueError("rgbPins should have 3 pins [red, green, blue]")

        if name not in self.led_strips:
            self.led_strips[name] = ILedStrip(red=pins[0], green=pins[1], blue=pins[2])


def get_hardware(name):
    return HardwareFactory.manager.get_hardware(name)

def clear_hardware():
    return HardwareFactory.manager.clear()
