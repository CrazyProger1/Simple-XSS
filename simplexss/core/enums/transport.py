from enum import Enum


class Transport(str, Enum):
    WEBSOCKET = 'websocket'
    HTTP = 'http'
