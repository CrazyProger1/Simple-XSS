import inspect

from .types import (
    BaseTransportAPI,
    BaseEvent,
    Endpoint,
    BaseClient
)
from .logging import logger
from ..data import Environment


class CommonTransportAPI(BaseTransportAPI):
    def __init__(self):
        self._payload = None
        self._endpoints = {}
        self._client_events = {}
        self._env = None

    @property
    def payload(self) -> str:
        if self._payload is None:
            raise ValueError('Payload not bound')

        return self._payload

    @property
    def environment(self) -> Environment:
        return self._env

    def bind_payload(self, payload: str):
        if not isinstance(payload, str):
            raise TypeError('Payload must be a string JS js')

        self._payload = payload
        logger.debug(f'apicall: Bound payload: {payload}')

    def bind_environment(self, env: Environment):
        self._env = env

    def endpoint(self, event: str, endpoint: Endpoint):
        self._endpoints[event] = endpoint
        logger.debug(f'apicall: Endpoint bound on event {event}: {endpoint}')

    async def send_event(self, client: BaseClient, event: BaseEvent):
        events = self._client_events.get(client, [])
        events.append(event)
        self._client_events[client] = events
        logger.debug(f'apicall: Event send to {client}: {event}')

    async def handle_event(self, client: BaseClient, event: BaseEvent):
        endpoint = self._endpoints.get(event.name)

        if not endpoint:
            return

        if inspect.iscoroutinefunction(endpoint):
            result = await endpoint(client, event)
        else:
            result = endpoint(client, event)

        if result is not None:
            if isinstance(result, BaseEvent):
                await self.send_event(client, event)

    def pop_event(self, client: BaseClient) -> BaseEvent | None:
        try:
            events = self._client_events.get(client)

            if events:
                return events.pop(0)
        except KeyError:
            return None
