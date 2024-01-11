import datetime
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from starlette.responses import StreamingResponse

from src.api.auth import get_current_user
from src.crud.contact import contact_crud
from src.db.session import get_async_session
from src.utils import responses

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/export",
    responses=responses,
)
async def export_to_excel(
        # auth: auth_dependency,
        db: AsyncSession = Depends(get_async_session),
):
    contacts = await contact_crud.get_contacts(db=db)
    data = [
        {
            "id": contact.id,
            "lead_name": contact.lead_name,
            "lead_company": contact.lead_company,
            "linkedin_profile": contact.linkedin_profile,
            "contact": contact.contact,
            "status": contact.status.value
        }
        for contact in contacts
    ]
    df = pd.DataFrame.from_records(data)

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name='Sheet1')
    excel_file.seek(0)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}"
    return StreamingResponse(excel_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={'Content-Disposition': f'attachment; filename={filename}.xlsx'})
