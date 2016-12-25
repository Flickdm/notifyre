#!/usr/bin/env python3
import sys, logging
import threading, asyncore

from BT import BTServer
from HW import Hardware
from WEB import create_app

logging.basicConfig(
            filename='notifyre-server.log',
            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            datefmt='%m-%d %H:%M',
            level=logging.DEBUG
            )

def run_bluetooth(hw):
    btserver = BTServer(hardware = hw, uuid = "4db81427-c67c-48a9-8be8-e9ae540f8e99", service_name = "Notifyre Server")
    asyncore.loop(timeout=30.0)

def run_web(hw):
    app = create_app(hw, __name__)
    app.run(host='0.0.0.0')

def main(argv):
    print("Notifyre Server")

    hw = Hardware()
    hw.create_output_device("power", 25)
    hw.create_led_strip("leds", [18, 23, 24])

    threading.Thread(target=run_bluetooth, args=(hw,)).start()
    run_web(hw)

if __name__ == "__main__":
    main(sys.argv)
