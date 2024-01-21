import datetime
from io import BytesIO
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from src.api.auth import get_current_user
from src.crud.contact import contact_crud
from src.db.db import get_db
from src.utils import responses

router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


@router.get(
    "/export",
    responses=responses,
)
async def export_to_excel(
        db: db_dependency,
        auth: auth_dependency,
):
    """Export contacts to an Excel file"""
    contacts = await contact_crud.get_contacts(db=db)
    data = [
        {
            "id": contact.id,
            "lead_name": contact.lead_name,
            "linkedin_profile": contact.linkedin_profile,
            "next_contact": contact.next_contact,
            "status": contact.status.split('.')[-1]
        }
        for contact in contacts
    ]
    df = pd.DataFrame.from_records(data)

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name='Sheet1')
    excel_file.seek(0)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"export_file_{timestamp}"
    return StreamingResponse(
        excel_file,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}.xlsx'}
    )
