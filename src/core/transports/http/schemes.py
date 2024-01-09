from ..schemes import BaseClientScheme, BaseEventScheme


class ClientScheme(BaseClientScheme):
    user_agent: str


class EventScheme(BaseEventScheme):
    pass


class EventReadScheme(EventScheme):
    pass


class EventCreateScheme(EventScheme):
    pass
