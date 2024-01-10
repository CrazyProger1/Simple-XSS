from enum import Enum


class GraphicMode(int, Enum):
    CLI = 1
    GUI = 2


class Protocol(str, Enum):
    HTTP = 'http'
    WEBSOCKET = 'websocket'
