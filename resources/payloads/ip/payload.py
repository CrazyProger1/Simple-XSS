from simplexss.api import (
    BasePayload,
    BaseTransport,
    BaseIOManager,
)


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Stealer'
    VERSION = '0.0.1'
    PROTOCOLS = {
        'http',
        'websocket'
    }

    @property
    def payload(self) -> str:
        pass

    async def print_event(self, event):
        print(event)

    def bind_transport(self, transport: BaseTransport):
        super().bind_transport(transport)

        self.transport.endpoint(self.print_event)

    def bind_io(self, io: BaseIOManager):
        super().bind_io(io)
