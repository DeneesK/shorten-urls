import pytest
import pytest_asyncio
from aiohttp import ClientSession

from main import app
from config import tests_settings


@pytest_asyncio.fixture
async def aiohttp_session():
    async with ClientSession() as session:
        yield session


@pytest.fixture
def create_url(aiohttp_session):
    async def inner(url: str):
        path = tests_settings.base_path + app.url_path_for('shorten_url')
        async with aiohttp_session.post(path, json={'url': url}) as resp:
            url_data = await resp.json()
        return url_data
    return inner
