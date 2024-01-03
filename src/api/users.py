from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import get_current_user
from src.crud.profile import profile_crud
from src.db.session import get_async_session
from src.schemas.profile import ProfileSchemaRead
from src.utils import responses

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/linkedin",
    response_model=ProfileSchemaRead,
    responses=responses,
)
async def get_linkedin_profile(
    auth: auth_dependency,
    profile_url: str,
    db: AsyncSession = Depends(get_async_session),

):
    """Get user`s LinkedIn profile"""
    profile = await profile_crud.get_profile(db=db, profile_url=profile_url)

    if profile:
        return profile
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")