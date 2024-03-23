import json
from functools import cache

from fastapi import Request

from .schemas import Client


@cache
def get_client(**data) -> Client:
    return Client.model_validate(data)


def get_fingerprint(request: Request) -> int:
    return hash(json.dumps({
        'user_agent': request.headers.get('user-agent'),
        'accept_language': request.headers.get('accept-language'),
        'remote_address': request.client.host,
        'cookies': request.cookies,
    }))


async def authenticate(request: Request) -> Client:
    fingerprint = get_fingerprint(request)
    return get_client(
        fingerprint=fingerprint,
        origin=request.client.host,
        user_agent=request.headers.get('user-agent')
    )
