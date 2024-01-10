from src.utils import network


def is_valid_port(port: int | str | None) -> bool:
    if isinstance(port, str):
        if not port.isdigit():
            return False
        port = int(port)
    if port is None:
        return True
    return network.validate_port(port=port)


def is_valid_host(host: str | None) -> bool:
    if host is None:
        return True
    return network.validate_host(host=host)


def is_valid_public_url(url: str) -> bool:
    if url is None:
        return True
    return network.validate_url(url=url)
