from http import HTTPStatus

import pytest

from main import app
from config import tests_settings


@pytest.mark.asyncio
async def test_create_shorten_url(aiohttp_session):
    path = tests_settings.base_path + app.url_path_for('ping')
    async with aiohttp_session.get(path) as resp:
        assert HTTPStatus.OK == resp.status
