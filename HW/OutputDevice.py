from gpiozero import OutputDevice
import logging

logger = logging.getLogger(__name__)

class IOutputDevice(object):
    def __init__(self, pin):
        self._output_device = OutputDevice(pin)
        self._is_output_device_on = False

    def set_on(self):
        self._output_device.on()
        self._is_output_device_on = True

    def set_off(self):
        self._output_device.off()
        self._is_output_device_on = False

    def toggle(self):
        if not self._is_output_device_on:
            self.set_on()
        else:
            self.set_off()

    def get_status(self):
        return self._is_output_device_on
