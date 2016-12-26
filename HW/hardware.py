from gpiozero import RGBLED, OutputDevice
import logging, weakref

from .led_strip import led_strip
from .output_device import output_device

logger = logging.getLogger(__name__)


class Cached_Hardware_Manager(object):
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_hardware(self, name):
        if name not in self._cache:
            hw = Hardware_Factory(name)
            self._cache[name] = hw
        else:
            hw = self._cache[name]

        return hw

    def clear(self):
        self._cache.clear()

class Hardware_Factory(object):
    manager = Cached_Hardware_Manager()

    def __init__(self, name):
        self.name = name
        self.output_devices = {};
        self.led_strips = {}

    def create_output_device(self, name="pwr", pin=25):
        if name not in self.output_devices:
            output_object = output_device(OutputDevice(pin))
            self.output_devices[name] = output_object

    def create_led_strip(self, name="leds", pins=[18, 23, 24]):

        if len(pins) != 3:
            raise ValueError("rgbPins should have 3 pins [red, green, blue]")

        if name not in self.led_strips:
            ledStrip_object = led_strip(RGBLED(red=pins[0], green=pins[1], blue=pins[2]))
            self.led_strips[name] = ledStrip_object

def get_hardware(name):
    return Hardware_Factory.manager.get_hardware(name)
