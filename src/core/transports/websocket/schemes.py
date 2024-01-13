from ..schemes import BaseClient, BaseEvent


class WebsocketClient(BaseClient):
    user_agent: str
    fingerprint: int

    def __hash__(self):
        return self.fingerprint


class WebsocketEvent(BaseEvent):
    pass
