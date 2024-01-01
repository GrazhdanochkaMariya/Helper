from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_db

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/linkedin/{profile_url}")
async def get_linkedin_profile(
        profile_url: str,
        db: AsyncSession = Depends(get_db),
):
    # profile =
    # if profile_id not in linkedin_profiles:
    #     raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": f"Checking LinkedIn profile: {profile_url}"}