#!/usr/bin/env python
import sys, logging, asyncore

from BT import BTServer
from hardware import Hardware

def main(argv):
    print "Notifyre Server"

    logging.basicConfig(
                filename='notifyre-server.log',
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                level=logging.DEBUG
                )

    BTClients = {}

    hw = Hardware()
    hw.create_output_device("power", 25)
    hw.create_led_strip("leds", [18, 23, 24])
    btserver = BTServer(hardware = hw, uuid = "4db81427-c67c-48a9-8be8-e9ae540f8e99", service_name = "Notifyre Server")

    try:
        asyncore.loop(timeout=30.0)
    except KeyboardInterrupt:
        logging.info("Shutdown Initiated")
        print "Quitting"


if __name__ == "__main__":
    main(sys.argv)
