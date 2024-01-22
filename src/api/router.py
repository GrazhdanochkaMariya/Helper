from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dao import LeadContactDAO
from src.api.schema import ContactSchemaRead, ContactSchemaReadFull
from src.auth.dependencies import get_current_user
from src.models import TypeEnum, User
from src.utils import CONTACT_NOT_FOUND_MESSAGE, responses

router = APIRouter()


@router.get(
    "/check/contact/",
    response_model=ContactSchemaReadFull,
    responses=responses,
)
async def get_contact(
    linkedin_profile: str = Query(),
):
    """Get user by LinkedIn profile"""
    contact = await LeadContactDAO.select_one_or_none_filter_by(
        linkedin_profile=linkedin_profile
    )
    if contact:
        return contact

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=CONTACT_NOT_FOUND_MESSAGE
    )


@router.post(
    "/gs/changed",
    responses=responses,
)
async def process_google_sheets_updates(
    data: ContactSchemaRead,
    user: User = Depends(get_current_user),
):
    """Process updates from Google Sheets"""
    if data.status == TypeEnum.CONTACT:
        contact = await LeadContactDAO().select_one_or_none_filter_by(
            linkedin_profile=data.linkedin_profile
        )
        if not contact:
            await LeadContactDAO().add_rows(data=data)

    elif data.status == TypeEnum.DECLINED:
        await LeadContactDAO().delete_rows_filer_by(
            linkedin_profile=data.linkedin_profile
        )

    elif data.status == TypeEnum.DNM:
        await LeadContactDAO().update_status_by_linkedin_profile(
            linkedin_profile=data.linkedin_profile, status=data.status
        )
