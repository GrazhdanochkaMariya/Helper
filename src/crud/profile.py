from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.crud.base import CRUDBase
from src.models.users import LinkedInProfile
from src.schemas.profile import ProfileSchemaRead


class CRUDProfile(CRUDBase[LinkedInProfile, ProfileSchemaRead]):
    async def get_profile(
            self,
            db: AsyncSession,
            *,
            profile_url: str):
        """Get LinkedIn profile"""
        query = select(self.model).where(self.model.linkedin_url == profile_url)

        item = await db.execute(query)
        return item.scalars().one_or_none()


profile_crud = CRUDProfile(LinkedInProfile)
