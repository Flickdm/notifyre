 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 This server allows for a user to receive and control the
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
import os

from flask_script import Manager

from BT import BTServer
from HW import get_hardware
from WEB import create_app

app = create_app(__name__)
manager = Manager(app)

CONFIG = configparser.ConfigParser()
CONFIG.read('config.cfg')

logging.basicConfig(
    filename='notifyre-server.log',
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    level=logging.DEBUG
    )

def init_hardware():
    hardware = get_hardware("gpio")
    hardware.create_output_device("power", 25)
    hardware.create_led_strip("leds", [18, 23, 24])

@manager.command
def run_servers():
    """ Runs both servers on seperate threads """

    #Starts bluetooth server on new thread
    threading.Thread(target=run_bluetooth, daemon=True).start()

    #Starts Web Server on main thread
    run_web()


@manager.command
def run_bluetooth():
    """ Starts the Bluetooth Server """
    BTServer(uuid=CONFIG['bt']['uuid'], service_name=CONFIG['bt']['service_name'])
    asyncore.loop(timeout=30.0)

@manager.command
def run_web():
    """ Starts the Web Server """
    app.secret_key = os.urandom(12)
    app.run(host=CONFIG['web']['ip'], port=CONFIG['web']['port'])

if __name__ == "__main__":
    init_hardware()
    manager.run()
