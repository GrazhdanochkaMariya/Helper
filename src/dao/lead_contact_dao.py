from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schema import ContactSchemaRead
from src.dao.base import BaseDAO
from src.models import LeadContact


class LeadContactDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(model=LeadContact, session=session)

    async def update_status_by_linkedin_profile(
        self, linkedin_profile: str, status: str
    ):
        query = (
            update(self.model)
            .where(self.model.linkedin_profile == linkedin_profile)
            .values({"status": status})
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result

    async def create_contact(
        self, data: ContactSchemaRead | dict
    ):
        """Create a new contact"""
        obj_in_data = dict(data)
        new_item = self.model(**obj_in_data)

        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
