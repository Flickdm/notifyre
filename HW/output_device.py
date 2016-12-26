from gpiozero import OutputDevice
import logging

logger = logging.getLogger(__name__)

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
