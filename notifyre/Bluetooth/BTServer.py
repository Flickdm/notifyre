"""Asynchronous Bluetooth Server responsible for delegating bluetooth connections

Todo:
    Investigate BLE
"""
import logging
import asyncore
import bluetooth as BT

from notifyre import get_hardware
from .BTHandler import BTHandler


HARDWARE = get_hardware("gpio")
LOGGER = logging.getLogger(__name__)

class BTServer(asyncore.dispatcher):
    """
    This class is the server and delegates to the handler when a connection
    is made
    """
    def __init__(self, uuid, service_name, port=BT.PORT_ANY):
        """

        Args:
            uuid (str): Universally Unique Identifier
            service_name (str): Name of servie
            port (:obj:`bluetooth port`): dynamically assigned port
        """
        asyncore.dispatcher.__init__(self)

        if not BT.is_valid_uuid(uuid):
            raise ValueError("uuid %s is not valid", uuid)

        self.port = port
        self.uuid = uuid
        self.service_name = service_name
        self.set_socket(BT.BluetoothSocket(BT.RFCOMM))
        self.bind(("", port))
        self.listen(1)

        BT.advertise_service(
            self.socket,
            service_name,
            service_id=uuid,
            #service_clases = [uuid, SERIAL_PORT_CLASS],
            profiles=[BT.SERIAL_PORT_PROFILE]
        )

        port = self.socket.getsockname()[1]

        LOGGER.info("Waiting for connection on RFCOMM channel %d", port)

    def handle_accept(self):
        """When we pair with a device pass off to handler to wait for event
        """
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            LOGGER.debug("Incoming connection from %s", repr(addr[0]))
            BTHandler(socket=sock, server=self)

    def handle_command(self, handler, data):
        """ handle the json returned by the handler
        """
        if "on" in data:
            HARDWARE.output_devices["power"].set_on()
            HARDWARE.led_strips["leds"].set_color_hex("#0000FF")
            HARDWARE.led_strips["leds"].pulse()
        elif "off" in data:
            HARDWARE.output_devices["power"].set_off()
            HARDWARE.led_strips["leds"].set_color_hex("#000000")
        elif "pow" in data:
            HARDWARE.output_devices["power"].toggle()
        elif "ledo" in data:
            HARDWARE.led_strips["leds"].set_color_hex("#0000FF")
            HARDWARE.led_strips["leds"].pulse()
        elif "ledf" in data:
            HARDWARE.led_strips["leds"].set_color_hex("#000000")
        elif "#" in data:
            HARDWARE.led_strips["leds"].set_color_hex(data)
        elif "fade" in data:
            HARDWARE.led_strips["leds"].blue2red()
        else:
            HARDWARE.led_strips["leds"].set_color_word(data)
