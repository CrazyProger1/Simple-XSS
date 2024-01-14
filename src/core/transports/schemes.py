from pydantic import BaseModel


class BaseClient(BaseModel):
    origin: str


class BaseEvent(BaseModel):
    event: str
    data: dict = None
