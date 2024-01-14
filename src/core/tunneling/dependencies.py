from src.utils import di

from .factories import (
    BaseTunnelingServiceFactory,
    TunnelingServiceFactory
)


class TunnelingDependencyContainer(di.DeclarativeContainer):
    factory: BaseTunnelingServiceFactory = di.Singleton(TunnelingServiceFactory)
