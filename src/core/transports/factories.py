from functools import cache

from typeguard import typechecked

from src.utils import clsutils
from src.core.enums import Protocol
from .services import BaseTransportService


class TransportServiceFactory:
    @classmethod
    @typechecked
    def get_names(cls) -> set[str]:
        names = set()
        for subcls in clsutils.iter_subclasses(BaseTransportService):
            names.add(subcls.name)
        return names

    @classmethod
    @cache
    @typechecked
    def get_class(cls, name: str) -> type[BaseTransportService] | None:
        for subcls in clsutils.iter_subclasses(BaseTransportService):
            if name == subcls.name:
                return subcls

    @classmethod
    @cache
    @typechecked
    def get_protocol(cls, name: str) -> Protocol | None:
        service_class = cls.get_class(name=name)
        if service_class:
            return service_class.protocol

    @classmethod
    @typechecked
    def create(cls, name: str) -> BaseTransportService:
        service_class = cls.get_class(name=name)
        if not service_class:
            raise ValueError(f'Transport service {name} not found')

        return service_class()
