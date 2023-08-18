import inspect
import re
from functools import cache

from app.utils.cli import exceptions


@cache
def validate_host(host: str):
    """Checks if the given string can be a host"""

    if not re.match(r'^\w+$', str(host)):
        raise exceptions.ValidationError(f'Host is invalid: {host}')

    return True


@cache
def validate_port(port: int | str):
    """Checks if the given integer can be a port"""

    if isinstance(port, str) and port.isdigit():
        port = int(port)

    if not isinstance(port, int):
        raise exceptions.ValidationError(f'Port must be type of integer not {type(port).__name__}')

    if not 0 < port < 65536:
        raise exceptions.ValidationError('Port must be in range (0, 65536)')

    return True


@cache
def validate_url(url: str, protocols: list | tuple = ('http', 'https', 'ws', 'wss')):
    """Checks if the given string can be an url of some allowed protocols"""

    url = str(url)
    if not re.match(r'^\w+://\S+$', url):
        raise exceptions.ValidationError('Url has wrong format')

    if not any(url.startswith(proto) for proto in protocols):
        raise exceptions.ValidationError('Url has unallowed protocol')

    return True
