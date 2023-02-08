from sqlalchemy.ext.asyncio import AsyncSession


class DBObjectService:

    def __init__(self, session: AsyncSession):
        self.session = session
