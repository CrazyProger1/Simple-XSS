from ..types import BaseTransportService


class HttpService(BaseTransportService):
    name = 'Default HTTP Transport'
    protocol = 'http'
