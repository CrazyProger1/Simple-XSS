from src.utils import di
from .schemes import (
    BaseClientScheme,
    WebsocketClientScheme,
    BaseEventScheme,
    WebsocketEventScheme
)

from .connections import ClientConnection, WebsocketClientConnection

websocket_client_schema_dependency = di.Dependency(BaseClientScheme, default=WebsocketClientScheme)
websocket_event_schema_dependency = di.Dependency(BaseEventScheme, default=WebsocketEventScheme)
websocket_connection_class_dependency = di.Dependency(ClientConnection, default=WebsocketClientConnection)
