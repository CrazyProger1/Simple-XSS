from unittest import TestCase

from src.utils import di

injector = di.Injector()


class BaseService:
    pass


class Service(BaseService):
    pass


base_service = di.Dependency(BaseService)


class TestInjector(TestCase):
    def test_inject(self):
        injector.bind(base_service, Service())

        @injector.inject
        def test(service: BaseService = base_service):
            self.assertIs(service.__class__, Service)

        test()
