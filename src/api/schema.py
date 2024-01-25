from typing import Optional

from pydantic import BaseModel, field_validator


class ContactSchemaRead(BaseModel):
    """Schema for profile"""

    lead_name: str
    linkedin_profile: str
    next_contact: Optional[str]
    status: str

    @field_validator("status", mode="before")
    def convert_status_to_upper(cls, v):
        """Validator to convert status to uppercase"""
        return v.upper()


class ContactSchemaReadFull(ContactSchemaRead):
    """Schema for full profile"""

    id: int
