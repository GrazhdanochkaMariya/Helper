from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import get_current_user
from src.crud.contact import contact_crud
from src.db.db import get_db
from src.models.users import TypeEnum
from src.schemas.profile import ContactSchemaRead, ContactSchemaReadFull
from src.utils import CONTACT_NOT_FOUND_MESSAGE, responses

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/check/contact",
    response_model=ContactSchemaReadFull,
    responses=responses,
)
async def get_contact(
        db: db_dependency,
        auth: auth_dependency,
        linkedin_profile: str = Query(),
):
    """Get user by LinkedIn profile"""
    contact = await contact_crud.get_contact_by_profile(
        db=db,
        linkedin_profile=linkedin_profile
    )

    if contact:
        return contact
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CONTACT_NOT_FOUND_MESSAGE
        )


@router.delete(
    "/delete/contact",
    responses=responses,
)
async def delete_contact(
        db: db_dependency,
        auth: auth_dependency,
        linkedin_profile: str = Query()):
    """Delete contact from DB"""
    contact = await contact_crud.get_contact_by_profile(
        db=db,
        linkedin_profile=linkedin_profile
    )
    if contact:
        await contact_crud.delete_contact_by_profile(
            db=db,
            linkedin_profile=linkedin_profile
        )
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CONTACT_NOT_FOUND_MESSAGE
        )


@router.post(
    "/update/contact",
    responses=responses,
)
async def process_google_sheets_updates(
        db: db_dependency,
        auth: auth_dependency,
        data: ContactSchemaRead,

):
    """Process updates from Google Sheets"""

    contact = await contact_crud.get_contact_by_profile(
        db=db,
        linkedin_profile=data.linkedin_profile
    )
    if data.status == TypeEnum.CONTACT:
        if contact:
            await contact_crud.update_contact(
                db=db,
                new_data=data,
                contact_id=contact.id
            )
            return True

        else:
            new_contact = await contact_crud.create_contact(db=db, new_data=data)
            return new_contact

    if data.status == TypeEnum.DECLINED:
        if contact:
            await contact_crud.delete_contact_by_profile(
                db=db,
                linkedin_profile=contact.linkedin_profile
            )
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CONTACT_NOT_FOUND_MESSAGE
            )

    if data.status == TypeEnum.DNM:
        if contact:
            await contact_crud.update_contact_status(
                db=db,
                new_status=data.status,
                contact_id=contact.id
            )
            return True

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CONTACT_NOT_FOUND_MESSAGE
            )
