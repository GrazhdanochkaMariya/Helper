from typing import Optional

from pydantic import BaseModel, validator


class ContactSchemaRead(BaseModel):
    """Schema for profile"""

    lead_name: str
    linkedin_profile: str
    next_contact: Optional[str]
    status: str

    @validator('status', pre=True)
    def convert_status_to_upper(cls, v):
        """Validator to convert status to uppercase"""
        return v.upper()


class ContactSchemaReadFull(ContactSchemaRead):
    """Schema for full profile"""

    id: int
