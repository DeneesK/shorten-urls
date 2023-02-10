from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from .common import DBObjectService
from models.db_models import UrlModel, HistoryModel
from db.db import get_session


class UrlService(DBObjectService):
    async def create_shorten_url(self, url: str) -> UrlModel:
        new_url = UrlModel(original_url=url)
        new_history = HistoryModel(url_id=new_url.id)
        self.session.add_all((new_url, new_history))
        await self.session.commit()
        return new_url

    async def redirect(self, id_: str) -> UrlModel:
        resp = await self.session.execute(
            select(UrlModel, HistoryModel).join(HistoryModel, UrlModel.id == id_)
        )
        print(resp.all())
        await self.session.commit()
        return 1

    async def get_info(self, id_: str):
        history = await self.session.execute(
            select(HistoryModel).where(HistoryModel.url_id == id_)
        )
        result = history.scalars().all()
        return result[0]

    async def delete(self, id_: str):
        url = await self.session.get(UrlModel, id_)
        url.is_deleted = True
        self.session.add(url)
        await self.session.commit()
        return url


def get_url_service(
        session: AsyncSession = Depends(get_session)
) -> UrlService:
    return UrlService(session)
