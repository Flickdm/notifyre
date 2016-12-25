#!/usr/bin/env python3
import sys, logging
import threading, asyncore
import configparser

from BT import BTServer
from HW import get_hardware
from WEB import create_app

config = configparser.ConfigParser()
config.read('config.cfg')

logging.basicConfig(
            filename='notifyre-server.log',
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            level=logging.DEBUG
            )

def run_bluetooth():
    btserver = BTServer(uuid = config['bt']['uuid'], service_name = config['bt']['service_name'])
    asyncore.loop(timeout=30.0)

def run_web():
    app = create_app(__name__)
    app.run(host=config['web']['ip'], port=config['web']['port'])

def main(argv):
    print("Starting Notifyre Server")

    hw = get_hardware("gpio")
    hw.create_output_device("power", 25)
    hw.create_led_strip("leds", [18, 23, 24])

    threading.Thread(target=run_bluetooth, daemon=True).start()
    run_web()

if __name__ == "__main__":
    main(sys.argv)
