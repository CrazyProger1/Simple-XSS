from ..schemes import BaseClient, BaseEvent


class HTTPClient(BaseClient):
    user_agent: str
    fingerprint: int

    def __hash__(self):
        return self.fingerprint


class HTTPEvent(BaseEvent):
    pass


class HTTPReadEvent(HTTPEvent):
    pass


class HTTPCreateEvent(HTTPEvent):
    pass
