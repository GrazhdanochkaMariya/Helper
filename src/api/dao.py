from sqlalchemy import update

from src.api.schema import ContactSchemaRead
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.models import LeadContact


class LeadContactDAO(BaseDAO):
    model = LeadContact

    @classmethod
    async def update_status_by_linkedin_profile(
        cls, linkedin_profile: str, status: str
    ):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.linkedin_profile == linkedin_profile)
                .values({"status": status})
            )
            result = await session.execute(query)
            await session.commit()
            return result

    @classmethod
    async def create_contact(
        cls, data: ContactSchemaRead
    ):
        """Create a new contact"""
        async with async_session_maker() as session:
            obj_in_data = dict(data)
            new_item = cls.model(**obj_in_data)

            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)

