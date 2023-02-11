import pytest_asyncio
from aiohttp import ClientSession


@pytest_asyncio.fixture
async def aiohttp_session():
    async with ClientSession() as session:
        yield session
