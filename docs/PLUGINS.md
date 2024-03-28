# Simple-XSS Plugins

Simple-XSS is designed to be expendable, almost every component can be replaced at runtime.

## DI-Containers

## Event-System

## Services

To add transport or tunneling service you can just implement service interface or inherit one of existing services.

### Transport

```python
from simplexss.api import BasePlugin

from simplexss.core.transports import BaseTransportService, BaseSession


class MyService(BaseTransportService):
    NAME = 'My HTTP Service'
    PROTOCOL = 'http'

    async def run(self, host: str, port: int, **kwargs) -> BaseSession:
        pass

    async def stop(self, session: BaseSession) -> None:
        pass


class Plugin(BasePlugin):
    pass
```

![Service Plugin](../resources/images/service1.png)

### Tunneling

```python
from simplexss.api import BasePlugin

from simplexss.core.tunneling import BaseTunnelingService, BaseSession


class MyService(BaseTunnelingService):
    NAME = 'My Tunneling Service'
    PROTOCOLS = {
        'http',
    }

    async def run(self, protocol: str, port: int) -> BaseSession:
        pass

    async def stop(self, session: BaseSession):
        pass


class Plugin(BasePlugin):
    pass
```

![service2.png](../resources/images/service2.png)