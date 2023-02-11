from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from .common import DBObjectService
from models.db_models import UrlModel, HistoryModel
from db.db import get_session


class UrlService(DBObjectService):
    async def create_shorten_url(self, url: str) -> UrlModel:
        new_url = UrlModel(original_url=url, history=[HistoryModel(),])
        self.session.add(new_url)
        await self.session.commit()
        return new_url

    async def redirect(self, id_: str) -> str | None:
        resp = await self.session.execute(
            update(HistoryModel).where(HistoryModel.url_id == id_)
            .values({'counter': select(HistoryModel.counter).where(HistoryModel.url_id == id_).scalar_subquery() + 1})
            .returning(select(UrlModel.original_url)
                       .filter(UrlModel.id == id_, UrlModel.is_deleted == False).scalar_subquery())  # noqa: E712
        )
        await self.session.commit()
        return resp.all()[0][0]

    async def get_info(self, id_: str) -> HistoryModel:
        history = await self.session.execute(
            select(HistoryModel).where(HistoryModel.url_id == id_)
        )
        result = history.scalars().all()
        return result[0]

    async def delete(self, id_: str) -> tuple:
        url = await self.session.execute(
            update(UrlModel).returning(UrlModel).where(UrlModel.id == id_).values({'is_deleted': True}))
        await self.session.commit()
        return url.all()[0]


def get_url_service(
        session: AsyncSession = Depends(get_session)
) -> UrlService:
    return UrlService(session)
