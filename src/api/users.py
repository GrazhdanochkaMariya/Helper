from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import get_current_user
from src.crud.contact import contact_crud
from src.db.db import get_db
from src.models.users import TypeEnum
from src.schemas.profile import ContactSchemaRead, ContactSchemaReadFull
from src.utils import responses

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/check/contact",
    response_model=ContactSchemaReadFull,
    responses=responses,
)
async def get_linkedin_profile(
        db: db_dependency,
        auth: auth_dependency,
        linkedin_profile: str = Query(),
):
    """Get user`s LinkedIn profile"""
    profile = await contact_crud.get_contact_by_profile(db=db, linkedin_profile=linkedin_profile)

    if profile:
        return profile
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.delete(
    "/delete/contact",
    responses=responses,
)
async def delete_contact(
        db: db_dependency,
        auth: auth_dependency,
        contact_id: int = Query(),
):
    """Delete contact from DB"""
    try:
        await contact_crud.delete_contact_by_id(db=db, contact_id=contact_id)
        return True
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Contact id should be an integer")


@router.post(
    "/update",
    responses=responses,
)
async def process_google_sheets_updates(
        db: db_dependency,
        auth: auth_dependency,
        data: ContactSchemaRead,

):
    """Process updates from Google Sheets."""

    contact = await contact_crud.get_contact_by_profile(db=db, linkedin_profile=data.linkedin_profile)
    if data.status == TypeEnum.CONTACT:
        if contact:
            await contact_crud.update_contact(db=db, new_data=data, contact_id=contact.id)
            return True

        else:
            new_contact = await contact_crud.create_contact(db=db, new_data=data)
            return new_contact

    if data.status == TypeEnum.DECLINED:
        if contact:
            await contact_crud.delete_contact_by_id(db=db, contact_id=contact.id)
            return True
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if data.status == TypeEnum.DNM:
        if contact:
            await contact_crud.update_contact_status(db=db, new_status=data.status, contact_id=contact.id)
            return True

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data")
