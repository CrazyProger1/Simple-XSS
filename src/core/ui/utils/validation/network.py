from src.utils import network


def is_valid_port(port: int | str | None) -> bool:
    if not port:
        return True
    if isinstance(port, str):
        if not port.isdigit():
            return False
        port = int(port)

    return network.validate_port(port=port)


def is_valid_host(host: str | None) -> bool:
    if not host:
        return True
    return network.validate_host(host=host)


def is_valid_public_url(url: str) -> bool:
    if not url:
        return True
    return network.validate_domain(url=url)
