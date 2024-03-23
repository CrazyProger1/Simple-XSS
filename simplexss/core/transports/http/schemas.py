from simplexss.core.api import (
    BaseEvent,
    BaseResponse,
    BaseClient
)


class Event(BaseEvent):
    pass


class Client(BaseClient):
    user_agent: str
    fingerprint: int

    def __hash__(self):
        return self.fingerprint
