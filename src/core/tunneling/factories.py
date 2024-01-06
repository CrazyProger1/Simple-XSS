from functools import cache

from typeguard import typechecked

from src.core.enums import Protocol
from src.utils import clsutils
from .services import BaseTunnelingService


class TunnelingServiceFactory:
    @classmethod
    @typechecked
    def get_names(cls, protocol: Protocol) -> set[str]:
        names = set()
        for subcls in clsutils.iter_subclasses(BaseTunnelingService):
            if protocol in subcls.protocols:
                names.add(subcls.name)
        return names

    @classmethod
    @cache
    @typechecked
    def get_class(cls, name: str) -> type[BaseTunnelingService] | None:
        for subcls in clsutils.iter_subclasses(BaseTunnelingService):
            if name == subcls.name:
                return subcls

    @classmethod
    @typechecked
    def create(cls, name: str) -> BaseTunnelingService:
        service_class = cls.get_class(name=name)
        if not service_class:
            raise ValueError(f'Tunneling service {name} not found')

        return service_class()
