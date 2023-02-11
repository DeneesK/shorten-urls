from http import HTTPStatus

import pytest


URL_ID = None


@pytest.mark.asyncio
async def test_create_shorten_url(aiohttp_session):
    data = {'url': 'http://www.google.com/'}
    async with aiohttp_session.post('http://url_service:8000/api/v1/', json=data) as resp:
        url_data = await resp.json()
        global URL_ID
        URL_ID = url_data['id']

    assert data['url'] == url_data['original_url']
    assert HTTPStatus.CREATED == resp.status


@pytest.mark.asyncio
async def test_redirect(aiohttp_session):
    async with aiohttp_session.get(f'http://url_service:8000/api/v1/{URL_ID}', allow_redirects=False) as resp:
        assert resp.headers['Location'] == 'http://www.google.com/'
        assert HTTPStatus.TEMPORARY_REDIRECT == resp.status


@pytest.mark.asyncio
async def test_url_status(aiohttp_session):
    async with aiohttp_session.get(f'http://url_service:8000/api/v1/{URL_ID}/status', allow_redirects=False) as resp:
        status_data = await resp.json()
    assert status_data['counter'] == 1
    assert status_data['url_id'] == URL_ID


@pytest.mark.asyncio
async def test_url_delete(aiohttp_session):
    async with aiohttp_session.delete(f'http://url_service:8000/api/v1/{URL_ID}', allow_redirects=False) as resp:
        url_data = await resp.json()

    assert url_data['is_deleted']
    assert url_data['id'] == URL_ID

    async with aiohttp_session.get(f'http://url_service:8000/api/v1/{URL_ID}', allow_redirects=False) as resp:
        assert HTTPStatus.GONE == resp.status
