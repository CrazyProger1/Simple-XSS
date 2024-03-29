from urllib.parse import urlparse

from .contants import (
    HOSTNAME_REGEX,
    DOMAIN_REGEX,
    URL_REGEX
)


def validate_port(port: int, raise_exceptions: bool = False) -> bool:
    valid = (0 <= port <= 65535)

    if not valid and raise_exceptions:
        raise ValueError(f'Port {port} is invalid')

    return valid


def validate_host(host: str, raise_exceptions: bool = False) -> bool:
    if HOSTNAME_REGEX.match(host):
        return True
    elif raise_exceptions:
        raise ValueError(f'Hostname {host} is invalid')
    return False


def validate_domain(domain: str, raise_exceptions: bool = False) -> bool:
    if DOMAIN_REGEX.match(domain):
        return True
    elif raise_exceptions:
        raise ValueError(f'Domain {domain} is invalid')
    return False


def validate_url(url: str, raise_exceptions: bool = False) -> bool:
    try:
        result = urlparse(url)
        scheme = result.scheme
        netloc = url.removeprefix(scheme + '://')

        if not all([scheme, netloc]):
            raise ValueError

        if ':/' in netloc:
            raise ValueError

        if ':' in netloc:
            netloc = netloc.split(':', 1)[0]

        if not validate_host(netloc):
            raise ValueError

    except ValueError:
        if raise_exceptions:
            raise ValueError(f'URL {url} is invalid')
        return False
    return True
