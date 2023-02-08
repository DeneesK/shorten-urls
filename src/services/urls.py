from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .common import DBObjectService
from models.db_models import UrlModel, HistoryModel
from db.db import get_session


class UrlService(DBObjectService):
    async def create_shorten_url(self, url: str) -> UrlModel:
        new_url = UrlModel(original_url=url)
        self.session.add(new_url)
        await self.session.commit()
        new_history = HistoryModel(url_id=new_url.id)
        self.session.add(new_history)
        await self.session.commit()
        return new_url

    async def get_by_id(self, id_: str) -> UrlModel:
        url = await self.session.get(UrlModel, id_)
        resp = await self.session.execute(
            select(HistoryModel).where(HistoryModel.url_id == id_)
        )
        history = resp.scalar()
        print(history)
        history.counter += 1
        self.session.add(history)
        await self.session.commit()
        return url

    async def get_info(self, id_: str):
        history = await self.session.execute(
            select(HistoryModel).where(HistoryModel.url_id == id_)
        )
        result = history.scalars().all()
        return result[0]


def get_url_service(
        session: AsyncSession = Depends(get_session)
) -> UrlService:
    return UrlService(session)
