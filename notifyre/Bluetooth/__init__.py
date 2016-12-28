""" Init file for importing Class """
from .BTServer import BTServer

def create_bluetooth_app(uuid=None, service_name=None):
    return BTServer(uuid=uuid, service_name=service_name)
