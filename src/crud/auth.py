from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.base import CRUDBase
from src.models.users import Admin
from src.schemas.auth import AdminSchemaCreate


class CRUDProfile(CRUDBase[Admin, AdminSchemaCreate, AdminSchemaCreate]):
    async def create_admin(
            self,
            db: AsyncSession,
            *,
            data
    ):
        """Create admin"""
        new_admin = self.model(**data)

        db.add(new_admin)

        await db.commit()
        await db.refresh(new_admin)

        return new_admin



    async def check_admin_name(
            self,
            db: AsyncSession,
            *,
            username: str
    ):
        """Check admin name"""
        query = select(self.model).where(self.model.username == username)

        item = await db.execute(query)
        return item.scalars().one_or_none()


    async def get_admin(
            self,
            db: AsyncSession,
            *,
            username: str,
            password: str
    ):
        """Get admin"""
        query = select(self.model).where(
            self.model.username == username,
            self.model.password == password
        )

        item = await db.execute(query)
        return item.scalars().one_or_none()


admin_crud = CRUDProfile(Admin)
