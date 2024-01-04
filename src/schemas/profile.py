from pydantic import BaseModel


class ContactSchemaRead(BaseModel):
    """Schema for profile"""

    id: int
    lead_name: str
    linkedin_profile: str
