from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import get_current_user
from src.crud.contact import contact_crud
from src.db.session import get_async_session
from src.schemas.profile import ContactSchemaRead, ContactSchemaReadFull
from src.utils import responses

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/check/contact",
    response_model=ContactSchemaReadFull,
    responses=responses,
)
async def get_linkedin_profile(
        # auth: auth_dependency,
        profile_url: str = Query(),
        db: AsyncSession = Depends(get_async_session),

):
    """Get user`s LinkedIn profile"""
    profile = await contact_crud.get_contact_by_profile(db=db, profile_url=profile_url)

    if profile:
        return profile
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.delete(
    "/delete/contact",
    responses=responses,
)
async def delete_contact(
        # auth: auth_dependency,
        contact_id: int = Query(),
        db: AsyncSession = Depends(get_async_session),
):
    """Delete contact from DB"""
    try:
        await contact_crud.delete_contact_by_id(db=db, contact_id=contact_id)
        return True
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Contact id should be an integer")


@router.patch(
    "/update",
    responses=responses,
)
async def process_google_sheets_updates(
        # auth: auth_dependency,
        data: ContactSchemaRead,
        db: AsyncSession = Depends(get_async_session),

):
    """Process updates from Google Sheets."""
    contact = await contact_crud.get_contact_by_profile(db=db, profile_url=data.linkedin_profile)

    if contact:
        await contact_crud.update_contact(db=db, new_data=data, contact_id=contact.id)
        return True

    else:
        new_contact = await contact_crud.create_contact(db=db, new_data=data)
        return new_contact
