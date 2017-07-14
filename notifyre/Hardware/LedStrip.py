"""
    Interface to GPIOZERO RGBLED
    Adds support for Hex and Generic words
"""

import logging
import re

from gpiozero import RGBLED

LOGGER = logging.getLogger(__name__)

class ILedStrip(object):
    """
    Interface to GPIOZERO RGBLED
    Adds support for Hex and Generic words such as:

    "none", "red", "green", "blue", "purple", "yellow"
    "aqua", "orange", "magenta", "white"


    """
    def __init__(self, red, green, blue):
        """
        sets up the Interface

        Args:
            red (int):   GPIO Pin
            green (int): GPIO pin
            blue (int):  GPIO Pin
        """
        self._led_strip = RGBLED(red, green, blue)
        self._cur_color = "#0000FF"
        self._prev_color = "#0000FF"

        self._is_pulse = False;

        self._defined_colors = {
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
        }

    # Setter
    def set_on(self):
        """
        Turns RGB on sets to the defined color
        """
        self._is_pulse = False
        self._led_strip.color = self._cvt_hex(self._cur_color)

    # Setter
    def set_off(self):
        """
        Turns RGB off
        """
        self._is_pulse = False
        self._led_strip.off()

    # Setter
    def set_color_hex(self, color="#000000"):
        """
        Sets the color to hex or sets it to none if not valid hex
        """
        if self._is_valid_hex(color):
            self._led_strip.color = self._cvt_hex(color)
            self._prev_color = self._cur_color
            self._is_pulse = False
            self._cur_color = color

    # Setter
    def set_color_word(self, color="none"):
        """
        Set color to current word or sets it to none if it is not supported
        """
        self._led_strip.color = self._color_map(color)
        self._prev_color = self._cur_color
        self._is_pulse = False
        self._cur_color = self._color_map(color, return_tuple=False)

    # Getter
    def get_status(self):
        """
        returns if the led_strip is lit
        """
        if self._is_pulse:
            return True

        return self._led_strip.is_lit

    def get_pulse_status(self):
        """
        returns true if currently pulsing
        """
        return self._is_pulse

    def get_prev_color(self):
        """
        returns previous color
        """
        return self._color_map(self._prev_color, return_tuple=False)

    # Getter
    def get_defined_colors(self):
        """
        returns what colors are supported and which color it is currently set to
        """
        defined_colors = {}
        for color in self._defined_colors:
            hex_color = self._color_map(color, return_tuple=False)

            if hex_color == self._cur_color:
                defined_colors[color] = True
            else:
                defined_colors[color] = False

        return defined_colors

    def toggle(self):
        """
        Toggles between off and on
        """
        if not self.led_strip.is_lit:
            self.set_on()
        else:
            self.set_off()


    def pulse(self, fade_in_time=5, fade_out_time=5, off_color=(0, 0, 0)):
        on_color = self._cvt_hex(self._cur_color)
        self._is_pulse = True
        self._led_strip.pulse(
            fade_in_time=fade_in_time,
            fade_out_time=fade_out_time,
            on_color=on_color,
            off_color=off_color
            )

    def blue2red(self):
        self._led_strip.pulse(
            fade_in_time=10,
            fade_out_time=10,
            on_color=(1, 0, 0),
            off_color=(0, 0, 1)
            )


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
            LOGGER.debug("Exception in cvtHex")

    def _color_map(self, color, return_tuple=True):
        if return_tuple:
            return self._cvt_hex(
                self._defined_colors.get(color, "#000000")
                )
        else:
            return self._defined_colors.get(color, "#000000")

    def _is_valid_hex(self, colorInHex):
        _rgbstring = re.compile(r'#[a-fA-F0-9]{6}$')
        return bool(_rgbstring.match(colorInHex))
