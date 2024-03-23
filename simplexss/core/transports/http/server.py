import asyncio
import threading

import uvicorn
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException
)
from starlette.middleware.cors import CORSMiddleware

from simplexss.core.api import (
    BaseTransport,
    BaseResponse,
)

from .schemas import (
    Event,
    Client
)
from .types import BaseHTTPServer
from .auth import authenticate
from ..exceptions import (
    TransportError,
    AddressInUseError
)


class FastAPIServer(BaseHTTPServer):
    def __init__(self, app: FastAPI = None):
        self._running = False
        self._app = app
        self._thread = None
        self._api: BaseTransport | None = None
        self._uvicorn_server: uvicorn.Server | None = None
        self._events = {}

        if app is None:
            self._app = FastAPI()

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

    def _register_endpoints(self):
        self._app.get('/script.js', status_code=200)(self._read_payload)
        self._app.get('/event', status_code=200, response_model=Event)(self._read_event)
        self._app.post('/event', status_code=200, response_model=BaseResponse)(self._handle_event)

    async def _read_payload(self, client: Client = Depends(authenticate)):
        self._events[client] = []
        return await self._api.handle_event(
            client=client,
            event=Event(
                name='payload'
            )
        )

    async def _read_event(self, client: Client = Depends(authenticate)):
        events = self._events.get(client)

        while not events:
            events = self._events.get(client)
            await asyncio.sleep(0.1)

        return events.pop()

    async def _handle_event(self, event: Event, client: Client = Depends(authenticate), ):
        return await self._api.handle_event(
            client=client,
            event=event
        )

    def _run_uvicorn(self, host: str, port: int):
        try:
            config = uvicorn.Config(app=self._app, host=host, port=port)
            self._uvicorn_server = uvicorn.Server(config)
            self._uvicorn_server.run()
        except SystemExit:
            raise AddressInUseError('Error')

    async def run(self, host: str, port: int, api: BaseTransport):
        assert not self._running
        self._running = True
        self._api = api

        self._thread = threading.Thread(
            target=self._run_uvicorn,
            args=(host, port),
            daemon=True
        )
        self._thread.start()

    async def stop(self):
        self._uvicorn_server.should_exit = True
        self._thread.join()
        self._running = False
