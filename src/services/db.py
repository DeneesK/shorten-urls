from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .common import DBObjectService
from db.db import get_session


class DBService(DBObjectService):
    async def ping_db(self):
        try:
            _ = await self.session.execute('SELECT 1')
        except Exception:
            return False
        return True


def get_db_service(
        session: AsyncSession = Depends(get_session)
) -> DBService:
    return DBService(session)
