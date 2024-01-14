import asyncio
from typing import Callable

import uvicorn
from fastapi import FastAPI, Request, responses
from starlette.middleware.cors import CORSMiddleware

from typeguard import typechecked

from .utils import get_fingerprint
from ..schemes import HTTPCreateEvent, HTTPReadEvent, HTTPClient
from ...exceptions import AddressInUseError, ServerAlreadyRunningError
from ...schemes import BaseClient, BaseEvent
from ...servers import BaseServer


class HTTPServer(BaseServer):
    def __init__(self):
        self._listeners = []
        self._clients: dict[int, BaseClient] = {}
        self._client_events: dict[BaseClient: list[BaseEvent]] = {}

        self._app = FastAPI()
        self._uvicorn_server = None
        self._running = False

        self._configure_app()
        self._register_endpoints()

    def _configure_app(self):
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    async def _call_listeners(self, client: BaseClient, event: BaseEvent):
        for listener in self._listeners:
            try:
                asyncio.create_task(listener(self, client, event))
            except Exception as e:
                print(type(e), e)

    def _authenticate(self, request: Request):
        fingerprint = get_fingerprint(request=request)
        if not self._clients.get(fingerprint):
            client = HTTPClient(
                origin=request.client.host,
                user_agent=request.headers.get('user-agent'),
                fingerprint=fingerprint
            )
            self._clients[fingerprint] = client
            self._client_events[client] = []

        return self._clients[fingerprint]

    def _pop_client_event(self, client: BaseClient) -> BaseEvent:
        events = self._client_events.get(client)
        if len(events) > 0:
            return events.pop(0)

    def _add_client_event(self, client: BaseClient, event: BaseEvent):
        events = self._client_events.get(client)
        if not event:
            raise
        events.append(event)

    async def _read_payload(self, request: Request):
        client = self._authenticate(request=request)
        return responses.HTMLResponse(content='alert(1)', media_type='text/javascript')

    async def _read_event(self, request: Request):
        client = self._authenticate(request=request)
        event = None

        while not event:
            event = self._pop_client_event(client=client)
            await asyncio.sleep(1)

        return HTTPReadEvent.model_validate(event.model_dump())

    async def _handle_event(self, request: Request, event: HTTPCreateEvent):
        client = self._authenticate(request=request)
        await self._call_listeners(client=client, event=event)
        return event

    def _register_endpoints(self):
        self._app.get('/script.js', status_code=200)(self._read_payload)
        self._app.get('/event', response_model=HTTPReadEvent, status_code=200)(self._read_event)
        self._app.post('/event', response_model=HTTPCreateEvent, status_code=200)(self._handle_event)

    async def _run_uvicorn(self, host: str, port: int):
        try:
            config = uvicorn.Config(app=self._app, host=host, port=port)
            self._uvicorn_server = uvicorn.Server(config)
            await self._uvicorn_server.serve()
        except SystemExit:
            raise AddressInUseError(host=host, port=port)

    @typechecked
    async def send(self, client: HTTPClient, event: BaseEvent):
        self._add_client_event(client=client, event=event)

    @typechecked
    def add_listener(self, callback: Callable[["BaseServer", BaseClient, BaseEvent], any]):
        self._listeners.append(callback)

    @typechecked
    async def run(self, host: str, port: int):
        if self._running:
            raise ServerAlreadyRunningError()

        self._running = True
        asyncio.create_task(self._run_uvicorn(host=host, port=port))

    async def stop(self):
        if self._uvicorn_server:
            await self._uvicorn_server.shutdown()
