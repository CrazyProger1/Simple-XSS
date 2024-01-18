from enum import Enum


class GraphicMode(int, Enum):
    GUI = 1


class Protocol(str, Enum):
    HTTP = 'http'
    WEBSOCKET = 'websocket'
