from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.base import CRUDBase
from src.models.users import Contact
from src.schemas.profile import ContactSchemaRead


class CRUDProfile(CRUDBase[Contact, ContactSchemaRead, ContactSchemaRead]):
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

    async def get_contacts(
            self,
            *,
            db: AsyncSession,
    ):
        """Get contacts"""
        query = select(self.model)

        items = await db.execute(query)
        return items.scalars().all()

    async def update_contact(self, db: AsyncSession, *, new_data: ContactSchemaRead, contact_id: int):
        """Update contact by id"""
        new_data_dict = new_data.dict()
        query = (update(self.model).where(self.model.id == contact_id).
                 values(**new_data_dict))

        await db.execute(query)
        await db.commit()

    async def create_contact(
        self, db: AsyncSession, *, new_data: ContactSchemaRead
    ):
        """Create a new contact"""
        obj_in_data = jsonable_encoder(new_data)
        new_item = self.model(**obj_in_data)

        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

        return new_item


contact_crud = CRUDProfile(Contact)
