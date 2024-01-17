from src.api.payloads import BasePayload


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Logger'
    VERSION = '0.1'
    TRANSPORTS = {
        'http',
        'websocket'
    }

    async def on_event(self, server, client, event):
        if event.name == 'ip':
            await self.io.print('IP:', event.data.get('ip'))

    @property
    def payload(self) -> str:
        return 'alert("IP LOGGER!")'
