from pydantic import BaseModel


class BaseClient(BaseModel):
    origin: str


class BaseEvent(BaseModel):
    name: str
    data: dict = None
