from bluetooth import *
import logging, asyncore

from .BTHandler import BTHandler
from HW import get_hardware

hw = get_hardware("gpio")

logger = logging.getLogger(__name__)

class BTServer(asyncore.dispatcher):
    def __init__(self, uuid, service_name, port = PORT_ANY):
        asyncore.dispatcher.__init__(self)

        if not is_valid_uuid(uuid):
            raise ValueError("uuid %s is not valid" % uuid)

        self.port = port
        self.uuid = uuid
        self.service_name = service_name
        self.set_socket(BluetoothSocket(RFCOMM))
        self.bind(("", port))
        self.listen(1)

        advertise_service(
                    self.socket,
                    service_name,
                    service_id = uuid,
                    #service_clases = [uuid, SERIAL_PORT_CLASS],
                    profiles = [SERIAL_PORT_PROFILE]
                )

        port = self.socket.getsockname()[1]

        logger.info("Waiting for connection on RFCOMM channel %d" % port)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            logger.debug("Incoming connection from %s" % repr(addr[0]))
            handler = BTHandler(socket = sock, server = self)


    #def handle_command(self, handler, data):
    def handle_command(self, handler, data):
        if "on" in data:
            hw.output_devices["power"].on()
            hw.led_strips["leds"].set_color_hex("#0000FF")
            hw.led_strips["leds"].pulse()
        elif "off" in data:
            hw.output_devices["power"].off()
            hw.led_strips["leds"].set_color_hex("#000000")
        elif "pow" in data:
            hw.output_devices["power"].toggle()
        elif "ledo" in data:
            hw.led_strips["leds"].set_color_hex("#0000FF")
            hw.led_strips["leds"].pulse()
        elif "ledf" in data:
            hw.led_strips["leds"].set_color_hex("#000000")
        elif "#" in data:
            hw.led_strips["leds"].set_color_hex(data)
        elif "fade" in data:
            hw.led_strips["leds"].blue2red()
        else:
            hw.led_strips["leds"].set_color_word(data)
