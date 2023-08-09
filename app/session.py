from dataclasses import dataclass
from app.payload import Payload
from app.hook import Hook


@dataclass
class ClientSession:
    connection: any = None
    payload: Payload = None
    hook: Hook = None
