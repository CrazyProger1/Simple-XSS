from pydantic import BaseModel


class HookSchema(BaseModel):
    name: str
    transport: str
    author: str = 'unknown'
    description: str | None = None
    version: str = '0.1'
