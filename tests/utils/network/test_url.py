import pytest

from simplexss.utils.network import change_protocol


@pytest.mark.parametrize(
    "url, protocol, expected",
    [
        ("http://abc.com", "https", "https://abc.com"),
        ("http://abc.com", "wss", "wss://abc.com"),
        ("ws://abc.com", "wss", "wss://abc.com"),
    ],
)
def test_change_protocol(url, protocol, expected):
    assert change_protocol(url, protocol) == expected
