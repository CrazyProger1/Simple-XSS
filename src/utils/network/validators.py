import re

from typeguard import typechecked


@typechecked
def validate_port(port: int, raise_exceptions: bool = False) -> bool:
    valid = (0 <= port <= 65535)

    if not valid and raise_exceptions:
        raise ValueError(f'Port {port} is invalid')

    return valid


@typechecked
def validate_host(host: str, raise_exceptions: bool = False) -> bool:
    hostname_pattern = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")

    if hostname_pattern.match(host):
        return True
    elif raise_exceptions:
        raise ValueError(f'Hostname {host} is invalid')
    return False


@typechecked
def validate_domain(url: str, raise_exceptions: bool = False):
    url_pattern = re.compile(
        r'^(?!:\/\/)([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    if url_pattern.match(url):
        return True
    elif raise_exceptions:
        raise ValueError(f'URL {url} is invalid')
    return False
