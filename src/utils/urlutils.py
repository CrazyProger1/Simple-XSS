from urllib.parse import urlparse

from typeguard import typechecked


@typechecked
def change_protocol(url: str, protocol: str) -> str:
    urlinfo = urlparse(url)
    return url.replace(urlinfo.scheme, protocol)
