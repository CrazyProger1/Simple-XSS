from functools import cache
from typing import Iterable

from simplexss.utils.clsutils import iter_subclasses

from .types import (
    BaseTunnelingServiceFactory,
    BaseTunnelingService
)


class TunnelingServiceFactory(BaseTunnelingServiceFactory):
    def create(self, name: str) -> BaseTunnelingService:
        service = self.get_service(name=name)
        if service is None:
            raise ValueError(f'Service not found: {name}')

        return service()

    @cache
    def get_service(self, name: str) -> type[BaseTunnelingService] | None:
        for service in iter_subclasses(BaseTunnelingService):
            if service.name == name:
                return service

    def get_names(self, protocol: str) -> Iterable[str]:
        return {
            service.name
            for service in iter_subclasses(BaseTunnelingService)
        }
