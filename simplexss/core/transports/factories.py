from functools import cache
from typing import Iterable

from simplexss.utils.clsutils import iter_subclasses
from .types import (
    BaseTransportService,
    BaseTransportServiceFactory
)


class TransportServiceFactory(BaseTransportServiceFactory):
    def create(self, name: str) -> BaseTransportService:
        service = self.get_service(name=name)
        if service is None:
            raise ValueError(f'Service not found: {name}')

        return service()

    @cache
    def get_service(self, name: str) -> type[BaseTransportService] | None:
        for service in iter_subclasses(BaseTransportService):
            if service.name == name:
                return service

    def get_names(self) -> Iterable[str]:
        return {
            service.name
            for service in iter_subclasses(BaseTransportService)
        }
