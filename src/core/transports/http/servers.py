import asyncio
import json

import uvicorn
from fastapi import FastAPI, Request, responses
from fastapi.middleware.cors import CORSMiddleware

from .schemes import (
    EventReadScheme,
    EventCreateScheme,
    ClientScheme
)
from .sessions import HTTPSession
from ..servers import BaseServer
from .connections import HTTPConnection


class HTTPServer(BaseServer):
    def __init__(self, host: str, port: int):
        super(HTTPServer, self).__init__(host=host, port=port)

        self._app = FastAPI()
        self._uvicorn_server = None
        self._configurate_app()
        self._register_routes()
        self._session = HTTPSession(host=host, port=port)
        self._connections = {}

    def _configurate_app(self):
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self._app.middleware('http')(self._authenticate)

    def _get_fingerprint(self, request: Request) -> int:
        return hash(json.dumps({
            "user_agent": request.headers.get('user-agent'),
            "accept_language": request.headers.get("accept-language"),
            "remote_address": request.client.host,
        }))

    def _get_connection(self, fingerprint: int) -> HTTPConnection | None:
        return self._connections.get(fingerprint)

    def _register_routes(self):
        self._app.get('/script.js', status_code=200)(self._read_payload)
        self._app.get('/event', response_model=EventReadScheme, status_code=200)(self._read_event)
        self._app.post('/event', response_model=EventCreateScheme, status_code=200)(self._handle_event)

    async def _authenticate(self, request: Request, call_next):
        fingerprint = self._get_fingerprint(request=request)
        if not self._get_connection(fingerprint=fingerprint):
            self._connections[fingerprint] = HTTPConnection(ClientScheme(
                user_agent=request.headers.get('user-agent'),
                origin=request.client.host
            ))
        return await call_next(request)

    async def _read_payload(self):
        return responses.HTMLResponse(content='alert(1)', media_type='text/javascript')

    async def _read_event(self, request: Request):
        conn = self._get_connection(
            fingerprint=self._get_fingerprint(
                request=request
            ))

        event = conn.pop_event()

        while not event:
            await asyncio.sleep(1)

        return event

    async def _handle_event(self, request: Request, event: EventCreateScheme):
        await self._session.call_listeners(
            self._get_connection(
                fingerprint=self._get_fingerprint(
                    request=request
                )),
            event=event
        )
        return event

    @property
    def session(self):
        return self._session

    async def run(self):
        config = uvicorn.Config(app=self._app, host=self._host, port=self._port)
        self._uvicorn_server = uvicorn.Server(config)
        asyncio.create_task(self._uvicorn_server.serve())

    async def stop(self):
        await self._uvicorn_server.shutdown()
