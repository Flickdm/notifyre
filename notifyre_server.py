 #!/usr/bin/env python3
"""This server allows for a user to receive and control the
 raspberry pi's gpio pins over bluetooth (via json) and via web
 interface.

 Functionally the user should be able to receive phone notifcations
 that will control the leds so that the user knows they've received
 a notifcation even if the phone is silenced. This is especially
 useful for those with hearing impairments as this will represent a
 visual notifcation.

 Todo:
    Hardware should really be created in the servers and the pins saved
"""

import logging
import threading
import asyncore
import configparser

from BT import BTServer
from HW import get_hardware
from WEB import create_app

CONFIG = configparser.ConfigParser()
CONFIG.read('config.cfg')

logging.basicConfig(
    filename='notifyre-server.log',
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    level=logging.DEBUG
    )

def run_bluetooth():
    """Starts the Bluetooth Server """
    BTServer(uuid=CONFIG['bt']['uuid'], service_name=CONFIG['bt']['service_name'])
    asyncore.loop(timeout=30.0)

def run_web():
    """Starts the Web Server """
    app = create_app(__name__)
    app.run(host=CONFIG['web']['ip'], port=CONFIG['web']['port'])

def main():
    """Main Function

    Here we create our our hardware and start the servers
    """
    print("Starting Notifyre Server")

    hardware = get_hardware("gpio")
    hardware.create_output_device("power", 25)
    hardware.create_led_strip("leds", [18, 23, 24])

    threading.Thread(target=run_bluetooth, daemon=True).start()
    run_web()

if __name__ == "__main__":
    main()
