import inspect
import re

from functools import cache
from app.utils.cli import exceptions


@cache
def validate_host(host: str):
    if not re.match(r'^\w+$', host):
        raise exceptions.ValidationError(f'host is invalid: {host}')

    return True


@cache
def validate_port(port: int):
    if not isinstance(port, int):
        raise exceptions.ValidationError(f'port must be type of integer not {type(port).__name__}')

    if not 0 < port < 65536:
        raise exceptions.ValidationError('port must be in range (0, 65536)')

    return True
