from src.utils import di

from .server import HTTPServer
from ..servers import BaseServer


class HTTPTransportDependencyContainer(di.DeclarativeContainer):
    server: BaseServer = di.Factory(HTTPServer)
