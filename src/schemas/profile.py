from pydantic import BaseModel

from src.models.users import TypeEnum


class ContactSchemaRead(BaseModel):
    """Schema for profile"""

    lead_name: str
    linkedin_profile: str
    lead_company: str
    contact: str
    status: TypeEnum


class ContactSchemaReadFull(BaseModel):
    """Schema for full profile"""

    id: int
