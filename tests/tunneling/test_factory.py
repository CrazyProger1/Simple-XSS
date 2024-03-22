from abc import ABC

from simplexss.core.tunneling import (
    TunnelingServiceFactory,
    BaseTunnelingService
)


class Service(BaseTunnelingService, ABC):
    name = 'http'
    protocols = (
        'test_proto_1',
    )


class Service2(BaseTunnelingService):
    name = 'test2'
    protocols = (
        'test_proto_2',
    )

    async def run(self, protocol: str, port: int):
        pass

    async def stop(self, session):
        pass


def test_get_names():
    factory = TunnelingServiceFactory()
    names = tuple(factory.get_names('test_proto_1'))

    assert len(names) == 1
    assert 'http' in names


def test_get_service():
    factory = TunnelingServiceFactory()

    assert factory.get_service('test2') is Service2


def test_create_instance():
    factory = TunnelingServiceFactory()

    assert isinstance(factory.create('test2'), Service2)
