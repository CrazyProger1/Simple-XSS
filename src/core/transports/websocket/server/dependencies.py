from src.utils import di
from ..encoders import BaseEncoder, JSONEncoder


class WebsocketServerDependencyContainer(di.DeclarativeContainer):
    encoder: BaseEncoder = di.Factory(JSONEncoder)
