from gpiozero import RGBLED, OutputDevice
from gpiozero.pins.native import NativePin
import logging

logger = logging.getLogger(__name__)

class Hardware(object):
    def __init__(self):
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



class output_device(object):
    def __init__(self, output_device):
        self._output_device = output_device
        self._is_output_device_on = False

    def on(self):
        self._output_device.on()
        self._is_output_device_on = True

    def off(self):
        self._output_device.off()
        self._is_output_device_on = False

    def toggle(self):
        if not self._is_output_device_on:
            self.on()
        else:
            self.off()

class led_strip(object):
    def __init__(self, led_strip):
        self._led_strip = led_strip
        self._prev_led_color = "#000000"
        self._cur_color = "#FF0000"

    def on(self):
        self._led_strip.on()

    def off(self):
        self._led_strip.off()

    def pulse(self, fade_in_time=5, fade_out_time=5, on_color=(1,0,0), off_color=(0,0,0)):
        on_color = self._cvt_hex(self._cur_color)
        self._led_strip.pulse(fade_in_time=fade_in_time, fade_out_time=fade_out_time, on_color=on_color, off_color=off_color)

    def set_color_hex(self, color="#FF0000"):
        if len(color) == 7:
            self._led_strip.color = self._cvt_hex(color)
            self._cur_color = color

    def set_color_word(self, color="red"):
        self._led_strip.color = self._color_map(color)

    def _cvt_hex(self, colorInHex):
        """
        TODO: make this more reslient
        """
        try: 
            red = float(int(colorInHex[1:3], 16)) / 255
            green = float(int(colorInHex[3:5], 16)) / 255
            blue = float(int(colorInHex[5:], 16)) / 255

            return (red, green, blue)
        except:
            return self._cvt_hex(self._cur_color)
            logger.debug("Exception in cvtHex")

    def _color_map(self, color):
        return self._cvt_hex({
            "none":     "#000000",
            "red":      "#FF0000",
            "green":    "#00FF00",
            "blue":     "#0000FF",
            "purple":   "#FF00FF",
            "yellow":   "#FFFF00",
            "aqua":     "#00FFFF",
            "orange":   "#FF1000",
            "magenta":  "#FF0080",
            "white":    "#FFFFFF"
        }.get(color, "#FF0000"))

    def blue2red(self):
        self._led_strip.pulse(fade_in_time=10, fade_out_time=10, on_color=(1,0,0), off_color=(0,0,1))

    def notification_state(self, notification_type):
        """
            Notifcatins Blink and Switch colors based on type
        """
        pass


