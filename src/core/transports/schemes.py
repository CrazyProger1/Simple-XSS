from pydantic import BaseModel


class BaseClientScheme(BaseModel):
    origin: str


class BaseEventScheme(BaseModel):
    event: str
    data: dict


class EventScheme(BaseEventScheme):
    pass
