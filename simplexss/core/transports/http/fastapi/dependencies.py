from typing import Annotated

from fastapi import (
    Request,
    Header
)

from .services import (
    get_client,
    generate_token
)


async def authenticate(
        request: Request,
        user_agent: Annotated[str | None, Header()] = None,
        authorization: Annotated[str | None, Header()] = None,
):
    if not authorization:
        authorization = generate_token()

    client = get_client(
        origin=request.client.host,
        user_agent=user_agent,
        token=authorization,
    )
    return client
