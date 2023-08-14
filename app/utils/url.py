import re

from functools import cache


@cache
def convert_url(url: str, protocol: str = 'wss') -> str:
    url = str(url)

    pattern = r'\w+://'

    if not re.match(pattern, url):
        return f'{protocol}://{url}'
    return url.replace(re.findall(pattern, url)[0], f'{protocol}://')
