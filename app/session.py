from dataclasses import dataclass
from app.payload import Payload
from app.hook import Hook


@dataclass
class ClientSession:
    connection: any = None
    payload: Payload = None
    hook: Hook = None

    def __hash__(self):
        return hash(self.connection)

    def __eq__(self, other):
        if isinstance(other, ClientSession):
            return self.connection == other.connection
        return False
