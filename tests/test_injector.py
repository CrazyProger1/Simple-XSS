from unittest import TestCase

from src.utils import di

injector = di.Injector()


class BaseService:
    pass


class Service(BaseService):
    pass


serv_1 = di.Dependency(BaseService)


class TestInjector(TestCase):
    def test_inject(self):
        injector.bind(serv_1, Service())

        @injector.inject
        def test(service: BaseService = serv_1):
            self.assertIs(service.__class__, Service)

        test()
