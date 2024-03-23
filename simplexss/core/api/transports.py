import inspect

from .types import (
    BaseTransport,
    Endpoint,
    BaseEvent,
    BaseResponse
)


class APITransport(BaseTransport):

    def __init__(self):
        self._endpoints = {}

    def endpoint(self, event: str, endpoint: Endpoint):
        self._endpoints[event] = endpoint

    async def handle_event(self, event: BaseEvent) -> BaseResponse:
        endpoint = self._endpoints.get(event.name)

        if endpoint is None:
            raise KeyError(f'No endpoint binding for event: {event.name}')

        if inspect.iscoroutinefunction(endpoint):
            response = await endpoint(event)
        else:
            response = endpoint(event)

        if not isinstance(response, BaseResponse):
            raise TypeError(f'Endpoint {event.name} returned invalid response: {response}')

        return response
