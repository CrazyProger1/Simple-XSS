from uuid import uuid4
from functools import cache

from .schemas import HTTPClient


@cache
def get_client(**data):
    return HTTPClient.model_validate(data)


def generate_token() -> str:
    return str(uuid4())
