from http import HTTPStatus

import pytest

from main import app
from config import tests_settings, URL_EXAMPLE


@pytest.mark.asyncio
async def test_create_shorten_url(aiohttp_session):
    data = {'url': URL_EXAMPLE}
    path = tests_settings.base_path + app.url_path_for('shorten_url')
    async with aiohttp_session.post(path, json=data) as resp:
        url_data = await resp.json()
    assert data['url'] == url_data['original_url']
    assert HTTPStatus.CREATED == resp.status


@pytest.mark.asyncio
async def test_redirect(aiohttp_session, create_url):
    url_obj = await create_url(url=URL_EXAMPLE)
    path = tests_settings.base_path + app.url_path_for('get_origin_url', shorten_url_id=url_obj['id'])

    async with aiohttp_session.get(path, allow_redirects=False) as resp:
        assert resp.headers['Location'] == URL_EXAMPLE
        assert HTTPStatus.TEMPORARY_REDIRECT == resp.status


@pytest.mark.asyncio
async def test_url_status(aiohttp_session, create_url):
    url_obj = await create_url(url=URL_EXAMPLE)

    path = tests_settings.base_path + app.url_path_for('get_origin_url', shorten_url_id=url_obj['id'])
    async with aiohttp_session.get(path, allow_redirects=False) as resp:
        assert HTTPStatus.TEMPORARY_REDIRECT == resp.status

    path = tests_settings.base_path + app.url_path_for('get_url_status', shorten_url_id=url_obj['id'])
    async with aiohttp_session.get(path) as resp:
        status_data = await resp.json()

    assert status_data['counter'] == 1
    assert status_data['url_id'] == url_obj['id']


@pytest.mark.asyncio
async def test_url_delete(aiohttp_session, create_url):
    url_obj = await create_url(url=URL_EXAMPLE)
    path = tests_settings.base_path + app.url_path_for('delete_url', shorten_url_id=url_obj['id'])

    async with aiohttp_session.delete(path, allow_redirects=False) as resp:
        url_data = await resp.json()

    assert url_data['is_deleted']
    assert url_data['id'] == url_obj['id']

    path = tests_settings.base_path + app.url_path_for('get_origin_url', shorten_url_id=url_obj['id'])
    async with aiohttp_session.get(path, allow_redirects=False) as resp:
        assert HTTPStatus.GONE == resp.status
