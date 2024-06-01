import pytest

from simplexss.utils.network import (
    validate_domain,
    validate_host,
    validate_port,
    validate_url,
)


@pytest.mark.parametrize(
    "url",
    [
        "https://google.com",
        "http://example.com",
        "wss://example.com",
        "ws://127.0.0.1:1234",
    ],
)
def test_validate_url(url):
    print(url)
    assert validate_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https:/google.com",
        "google.com",
    ],
)
def test_validate_invalid_url(url):
    assert not validate_url(url)


@pytest.mark.parametrize(
    "port",
    [
        0,
        65535,
    ],
)
def test_validate_port(port):
    assert validate_port(port)


@pytest.mark.parametrize(
    "port",
    [
        -1,
        65536,
    ],
)
def test_validate_invalid_port(port):
    assert not validate_port(port)
