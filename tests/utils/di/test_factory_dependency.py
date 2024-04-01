import pytest

from simplexss.utils.di import (
    containers,
    dependencies
)


class Service:
    pass


class Service2:
    pass


def functional_factory():
    return Service2()


@pytest.mark.parametrize('factory, base', [
    (Service, Service),
    (Service2, Service2),
    (functional_factory, Service2)
])
def test_factory(factory, base):
    class Container(containers.Container):
        my_factory = dependencies.Factory(factory)

    assert isinstance(Container.my_factory.value, base)


def test_factory_bind():
    class Container(containers.Container):
        factory = dependencies.Factory(Service)

    assert isinstance(Container.factory.value, Service)

    Container.factory.bind_factory(Service2)

    assert isinstance(Container.factory.value, Service2)
