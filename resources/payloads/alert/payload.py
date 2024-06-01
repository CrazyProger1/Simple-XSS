from simplexss.api import BaseClient, BaseEvent, BasePayload, render


class Payload(BasePayload):
    AUTHOR = "crazyproger1"
    DESCRIPTION = "Alerts your message when connection established."
    NAME = "Alert"
    VERSION = "0.0.1"

    async def on_connection(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f"Connection established: {client.origin}")

        text = await self.io.input("Text")

        return {"name": "alert", "data": {"text": text}}

    def bind_endpoints(self):
        self.transport.bind_endpoint("connection", self.on_connection)

    @property
    def payload(self) -> str:
        return render(
            self.directory,
            "payload.js",
        )
