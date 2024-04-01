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
    BaseClient,
    BaseEvent,
)
from simplexss.core.transports.exceptions import TransportError
from simplexss.utils.theads import thread
from simplexss.utils.network import (
    validate_host,
    validate_port
)
from .constants import TRANSPORT_JS_CODE
from .dependencies import authenticate
from ..types import (
    BaseHTTPTransportServer,
)


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

    def _get_full_payload(self, client: BaseClient) -> str:
        transport = Template(TRANSPORT_JS_CODE).render(
            token=client.token,
            environment=self._api.environment,
        )

        code = self._api.payload
        code = f'{transport}\n\n{code}'
        return code

    async def _read_payload(self, client: BaseClient = Depends(authenticate)):
        code = self._get_full_payload(client=client)
        await self._api.handle_event(client, BaseEvent(name='connection', data={}))
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

    def _check_errors(self):
        if not self._error_queue.empty():
            error = self._error_queue.get()
            raise error

    def _setup_api(self):
        self._api = CommonTransportAPI()

    @thread(daemon=True)
    def _run_server_in_thread(self):
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

    async def _run_server(self):
        self._server_thread = self._run_server_in_thread()

        await asyncio.sleep(0.5)
        self._check_errors()

    def _validate_params(self):
        validate_port(self._port, raise_exceptions=True)
        validate_host(self._host, raise_exceptions=True)

    async def run(self, host: str = None, port: int = None) -> BaseTransportAPI:
        if self._running:
            raise TransportError('Server is already running')

        self._host = host or self._host
        self._port = port or self._port

        self._validate_params()

        self._running = True

        self._setup_api()

        await self._run_server()
        return self._api

    async def stop(self):
        self._uvicorn_server.should_exit = True
        del self._server_thread
        self._running = False
