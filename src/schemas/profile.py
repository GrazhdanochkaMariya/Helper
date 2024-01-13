from datetime import datetime

from pydantic import BaseModel, validator


class ContactSchemaRead(BaseModel):
    """Schema for profile"""

    lead_name: str
    linkedin_profile: str
    next_contact: datetime
    status: str

    @validator('next_contact', pre=True)
    def parse_next_contact(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%d.%m.%Y')
        return v

    def convert_status_to_upper(cls, v):
        """Validator to convert status to uppercase"""
        return v.upper()


class ContactSchemaReadFull(ContactSchemaRead):
    """Schema for full profile"""

    id: int
