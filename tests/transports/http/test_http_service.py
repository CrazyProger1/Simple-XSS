import pytest

from simplexss.core.transports import BaseSession
from simplexss.core.transports.http import (
    HTTPSession,
    HTTPService
)


@pytest.mark.asyncio
async def test_http_service_run():
    service = HTTPService()
    session = await service.run(
        'localhost',
        4444
    )

    assert isinstance(session, BaseSession)
