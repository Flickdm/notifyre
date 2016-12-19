from bluetooth import *
import logging, asyncore

logger = logging.getLogger(__name__)

class BTHandler(asyncore.dispatcher):
    def __init__(self, socket, server):
        asyncore.dispatcher.__init__(self, socket)
        self._server = server
        self._data = ""

    def writable(self):
        """ 
            IMPORTANT: Overwrite the writable method so that cpu doesn't max out 
            NOTE: if there are characters in buffer it will freak out
        """

        return bool(self._data)

    def handle_read(self):

        try:
            data = self.recv(1204)
            if not data:
                return

            zero_char_index = data.find(';') # chr(0)
            if zero_char_index == -1:
                self._data += data
            else:
                self._data += data[:zero_char_index]
                self._handle_json()
        except IOError:
            # Closed by Peer -- EGAIN
            self.handle_close()

    def handle_close(self):
        logger.debug("Connection to device was lost")
        self.close()

    def _handle_json(self):
        self._server.handle_command(handler = self, data = self._data) 
        #clear 
        self._data = ""
