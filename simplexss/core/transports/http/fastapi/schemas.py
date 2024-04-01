from simplexss.core.transports import (
    BaseClient,
    BaseEvent,
)


class HTTPClient(BaseClient):
    token: str
    user_agent: str

    def __hash__(self) -> int:
        return hash(self.token)


class HTTPEvent(BaseEvent):
    pass
