class BTError(object):
    ERR_UKN         = 0x0
    ERR_UNKN_TYPE   = 0x1
    ERR_UNKN_PYLD   = 0x2

    ERROR_MSG = {
        ERR_UKN:        "Unknown error",
        ERR_UNKN_TYPE:  "Type of payload was uknown",
        ERR_UNKN_PYLD:  "Payload was empty"
    }

    @staticmethod
    def _send_error(handler, error = 0x0, error_msg):
        if len(error_msg) > 0:
            pass
