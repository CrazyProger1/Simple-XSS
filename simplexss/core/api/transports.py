import inspect

from .types import (
    BaseTransport,
    Endpoint,
    BaseEvent,
    BaseResponse, BaseClient
)


class APITransport(BaseTransport):

    def __init__(self):
        self._endpoints = {}

    def endpoint(self, event: str, endpoint: Endpoint):
        self._endpoints[event] = endpoint

    async def handle_event(self, client: BaseClient, event: BaseEvent) -> BaseResponse:
        endpoint = self._endpoints.get(event.name)

        if endpoint is None:
            raise KeyError(f'No endpoint binding for event: {event.name}')

        if inspect.iscoroutinefunction(endpoint):
            response = await endpoint(client, event)
        else:
            response = endpoint(client, event)

        if isinstance(response, dict):
            response = BaseResponse.model_validate(response)

        if response is None:
            response = BaseResponse()

        return response
