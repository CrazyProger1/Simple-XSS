from src.utils import di

from .factories import (
    BaseTransportServiceFactory,
    TransportServiceFactory
)


class TransportsDependencyContainer(di.DeclarativeContainer):
    factory: BaseTransportServiceFactory = TransportServiceFactory
