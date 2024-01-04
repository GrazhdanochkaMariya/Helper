from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.base import CRUDBase
from src.models.users import Contact
from src.schemas.profile import ContactSchemaRead


class CRUDProfile(CRUDBase[Contact, ContactSchemaRead]):
    async def get_contact_by_profile(
            self,
            db: AsyncSession,
            *,
            profile_url: str
    ):
        """Get contact by LinkedIn url"""
        query = select(self.model).where(self.model.linkedin_profile == profile_url)

        item = await db.execute(query)
        return item.scalars().one_or_none()

    async def delete_contact_by_id(
            self,
            db: AsyncSession,
            *,
            contact_id: int
    ):
        query = delete(self.model).where(self.model.id == contact_id)

        await db.execute(query)
        await db.commit()


contact_crud = CRUDProfile(Contact)
