from sqlalchemy import update

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
