from src.api.payloads import BasePayload


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Logger'
    VERSION = '0.1'
    TRANSPORT = {
        'http',
        'websocket'
    }
