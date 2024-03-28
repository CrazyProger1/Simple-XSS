import asyncio
import threading
import queue

import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
    Depends,
    responses,
    Request
)
from jinja2 import Template

from simplexss.core.transports import (
    BaseTransportAPI,
    CommonTransportAPI,
    BaseClient, BaseEvent,
)
from simplexss.utils.theads import thread
from .constants import TRANSPORT_JS_CODE
from .dependencies import authenticate
from ..types import (
    BaseHTTPTransportServer,
)
from simplexss.core.transports.exceptions import TransportError


class FastAPIServer(BaseHTTPTransportServer):
    def __init__(self, host: str = None, port: int = None, fastapi: FastAPI = None):
        self._running = False
        self._api: CommonTransportAPI | None = None
        self._fastapi = fastapi or FastAPI()
        self._server_thread: threading.Thread | None = None
        self._uvicorn_server: uvicorn.Server | None = None
        self._host: str = host
        self._port: int = port
        self._error_queue = queue.Queue()

        self._configure_fastapi()

    def _configure_fastapi(self):
        self._fastapi.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self._register_endpoints()

    def _register_endpoints(self):
        self._fastapi.get(
            '/.js',
            status_code=200,
        )(self._read_payload)

        self._fastapi.get(
            '/event',
            status_code=200,
            response_model=BaseEvent,
        )(self._read_event)

        self._fastapi.post(
            '/event',
            status_code=200,
        )(self._create_event)

    @thread(daemon=True)
    def _run_server(self):
        try:
            config = uvicorn.Config(
                app=self._fastapi,
                host=self._host,
                port=self._port
            )
            self._uvicorn_server = uvicorn.Server(config)
            self._uvicorn_server.run()

        except SystemExit:
            self._error_queue.put(TransportError(f'Address is already in use: {self._host}:{self._port}'))

    def _get_full_payload(self, client: BaseClient) -> str:
        transport = Template(TRANSPORT_JS_CODE).render(
            token=client.token,
            environment=self._api.environment,
        )

        code = self._api.payload
        try:
            code = code.format(
                transport=transport,
            )
        except KeyError:
            pass

        return code

    async def _read_payload(self, client: BaseClient = Depends(authenticate)):
        code = self._get_full_payload(client=client)
        return responses.HTMLResponse(
            content=code,
            media_type='text/javascript'
        )

    async def _read_event(self, client: BaseClient = Depends(authenticate)):
        event = self._api.pop_event(client)

        while not event:
            await asyncio.sleep(0.1)
            event = self._api.pop_event(client)

        return event

    async def _create_event(self, event: BaseEvent, client: BaseClient = Depends(authenticate)):
        await self._api.handle_event(client, event)

    async def _check_errors(self):
        pass

    async def run(self, host: str = None, port: int = None) -> BaseTransportAPI:
        if self._running:
            raise RuntimeError('Server is already running')

        self._host = host or self._host
        self._port = port or self._port

        assert self._host is not None
        assert self._port is not None

        self._running = True
        self._api = CommonTransportAPI()

        self._server_thread = self._run_server()

        await asyncio.sleep(0.1)
        if not self._error_queue.empty():
            error = self._error_queue.get()
            raise error

        return self._api

    async def stop(self):
        self._uvicorn_server.should_exit = True
        self._server_thread.join()
        self._running = False
