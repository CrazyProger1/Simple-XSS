import pytest

from simplexss.utils.di import (
    containers,
    dependencies
)


def test_singleton():
    class Service:
        pass

    class Container(containers.Container):
        singleton = dependencies.Singleton(Service)

    assert Container.singleton.value is Container.singleton.value
