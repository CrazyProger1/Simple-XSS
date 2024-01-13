from src.utils import di

from .server import WebsocketServer
from ..servers import BaseServer



class WebsocketTransportDependencyContainer(di.DeclarativeContainer):
    server: BaseServer = di.Factory(WebsocketServer)

