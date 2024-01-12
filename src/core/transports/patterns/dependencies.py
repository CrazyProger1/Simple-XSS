from src.utils import di
from .factories import TransportServiceFactory
from .encoders import BaseEncoder, JSONEncoder


class TransportsDependencyContainer(di.DeclarativeContainer):
    factory: TransportServiceFactory
    encoder_class: BaseEncoder = JSONEncoder
