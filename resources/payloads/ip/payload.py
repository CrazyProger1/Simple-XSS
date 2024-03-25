from simplexss.api import BasePayload


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Stealer'
    VERSION = '0.0.1'
    PROTOCOLS = {
        'http',
        'websocket'
    }
