from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_shorten_url(aiohttp_session):
    async with aiohttp_session.get('http://url_service:8000/api/v1/db/ping') as resp:
        assert HTTPStatus.OK == resp.status
