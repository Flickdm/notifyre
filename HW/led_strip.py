import logging

from gpiozero import RGBLED

LOGGER = logging.getLogger(__name__)

class led_strip(object):
    def __init__(self, red, green, blue ):
        self._led_strip = RGBLED(red, green, blue)
        self._prev_led_color = "#000000"
        self._cur_color = "#0000FF"
        self._is_led_strip_on = False

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

    def set_on(self):
        #self._led_strip.on()
        print(self._cur_color)
        self._led_strip.color = self._cvt_hex(self._cur_color)
        self._is_led_strip_on = True


    def set_off(self):
        self._led_strip.off()
        self._is_led_strip_on = False

    def toggle(self):
        if not self._is_led_strip_on:
            self.set_on()
        else:
            self.set_off()

    def pulse(self, fade_in_time=5, fade_out_time=5, on_color=(1, 0, 0), off_color=(0, 0, 0)):
        on_color = self._cvt_hex(self._cur_color)
        self._led_strip.pulse(
            fade_in_time=fade_in_time,
            fade_out_time=fade_out_time,
            on_color=on_color,
            off_color=off_color
            )

        self._is_led_strip_on = True

    def set_color_hex(self, color="#000000"):
        if len(color) == 7:
            self._is_led_strip_on = True

            if color == "#000000":
                self._is_led_strip_on = False

            self._led_strip.color = self._cvt_hex(color)
            self._cur_color = color

    def set_color_word(self, color="none"):

        self._cur_color = self._color_map(color, return_tuple=False)

        self._is_led_strip_on = True
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
            LOGGER.debug("Exception in cvtHex")

    def _color_map(self, color, return_tuple=True):
        if return_tuple:
            return self._cvt_hex(
                self._defined_colors.get(color, "#000000")
                )
        else:
            return self._defined_colors.get(color, "#000000")

    def blue2red(self):
        self._led_strip.pulse(
            fade_in_time=10,
            fade_out_time=10,
            on_color=(1, 0, 0),
            off_color=(0, 0, 1)
            )

        self._is_led_strip_on = True

    def get_status(self):
        return self._is_led_strip_on

    def get_defined_colors(self):
        defined_colors = {}
        for color in self._defined_colors:
            hex_color = self._color_map(color, return_tuple=False)

            if hex_color == self._cur_color:
                defined_colors[color] = True
            else:
                defined_colors[color] = False

        return defined_colors

    def notification_state(self, notification_type):
        """
            Notifcatins Blink and Switch colors based on type
        """
        pass
