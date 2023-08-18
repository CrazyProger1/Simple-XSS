from dataclasses import dataclass

from app.payload import Payload
from app.hook import Hook
from app.environment import Environment


@dataclass
class ClientSession:
    """Client session is created after the client has hooked"""

    connection: any = None
    payload: Payload = None
    hook: Hook = None
    environment: Environment = None

    def __hash__(self):
        return hash(self.connection)

    def __eq__(self, other):
        if isinstance(other, ClientSession):
            return self.connection == other.connection
        return False
