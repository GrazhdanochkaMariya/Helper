from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def select_all_filter(self, *args):
        query = select(self.model).filter(*args)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def select_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def select_all_filter_by(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def select_one_or_none_filter(self, *args):
        query = select(self.model).filter(*args)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def select_one_or_none_filter_by(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add_rows(self, **data):
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        await self.session.commit()
        return result

    async def delete_rows_filer(self, *args):
        query = delete(self.model).filter(*args)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_rows_filer_by(self, **kwargs):
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
