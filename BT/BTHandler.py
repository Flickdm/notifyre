"""Bluetooth Handler
"""

import logging
import asyncore

LOGGER = logging.getLogger(__name__)

class BTHandler(asyncore.dispatcher):
    """This class is the handler for the asychronous bluetooth server

    Todo:
        * Handle Json better
    """

    def __init__(self, socket, server):
        """__init__ method

        Args:
            socket (:obj:`bluetooth socket`): Socket created by the server so
                that we can communicate to phone
            server (:obj:`bluetooth server`): Instance of the server so that we
                can communicate back to the server
        """

        asyncore.dispatcher.__init__(self, socket)
        self._server = server
        self._data = ""

    def writable(self):
        """Called each time around the loop to check if an event occured.

        Note:
            Check to make sure that there are characters in buffer before
            attempt to write. If characters stay in buffer cpu will max out
        """

        return bool(self._data)

    def handle_read(self):
        """Called when the asynchronous loop detects that a read() call on the
        channel’s socket will succeed.

        add to self._data until we find a null character and call the
        handle_json
        """
        try:
            #receive data as 'utf-8'
            data = str(self.recv(1204), 'utf-8')
            if not data:
                return

            #add to self._data until we find a null character
            zero_char_index = data.find(';')#chr(0))
            if zero_char_index == -1:
                self._data += data
            else:
                self._data += data[:zero_char_index]
                self._handle_json()
        except IOError:
            #Closed by Peer -- EGAIN
            #if we don't do this a null character will be left in self._data
            #causing the cpu to max out
            self.handle_close()

    def handle_close(self):
        """Called when the socket is closed.
        """
        LOGGER.debug("Connection to device was lost")
        self.close()


    def _handle_json(self):
        """ self implemented json handler that passes the data back to server
        """
        self._server.handle_command(handler=self, data=self._data)
        #clear
        self._data = ""
