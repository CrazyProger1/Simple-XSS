from .types import (
    BaseTransportAPI,
    BaseEvent,
    Endpoint,
    BaseClient
)
from .logging import logger


class CommonTransportAPI(BaseTransportAPI):
    def __init__(self):
        self._payload = None
        self._endpoints = {}
        self._events = {}

    @property
    def payload(self) -> str:
        if self._payload is None:
            raise ValueError('Payload not bound')

        return self._payload

    @property
    def endpoints(self) -> dict:
        return self._endpoints

    @property
    def events(self) -> dict:
        return self._events

    def bind_payload(self, payload: str):
        if not isinstance(payload, str):
            raise TypeError('Payload must be a string JS code')

        self._payload = payload
        logger.debug(f'apicall: Bound payload: {payload}')

    def endpoint(self, event: str, endpoint: Endpoint):
        self._endpoints[event] = endpoint
        logger.debug(f'apicall: Endpoint bound on event {event}: {endpoint}')

    def send_event(self, client: BaseClient, event: BaseEvent):
        events = self._events.get(client, [])
        events.append(event)
        self._events[client] = events
        logger.debug(f'apicall: Event send to {client}: {event}')
