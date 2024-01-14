from abc import ABC, abstractmethod
from functools import cache

from typeguard import typechecked

from src.utils import clsutils
from src.core.enums import Protocol
from .services import BaseTransportService


class BaseTransportServiceFactory(ABC):
    @classmethod
    @abstractmethod
    def get_names(cls) -> set[str]: ...

    @classmethod
    @abstractmethod
    def get_transport_protocol(cls, name: str) -> Protocol: ...

    @classmethod
    @abstractmethod
    def get_class(cls, name: str) -> type[BaseTransportService] | None: ...

    @classmethod
    @abstractmethod
    def create(cls, name: str) -> BaseTransportService: ...


class TransportServiceFactory(BaseTransportServiceFactory):

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
    def get_transport_protocol(cls, name: str) -> Protocol:
        transport_class = cls.get_class(name)
        return transport_class.protocol

    @classmethod
    @cache
    @typechecked
    def get_class(cls, name: str) -> type[BaseTransportService] | None:
        for subcls in clsutils.iter_subclasses(BaseTransportService):
            if name == subcls.name:
                return subcls
        raise ValueError(f'Transport service class {name} not found')

    @classmethod
    @typechecked
    def create(cls, name: str) -> BaseTransportService:
        service_class = cls.get_class(name=name)
        if not service_class:
            raise ValueError(f'Transport service {name} not found')

        return service_class()
