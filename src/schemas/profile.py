from pydantic import BaseModel


class ProfileSchemaRead(BaseModel):
    """Schema for profile"""

    id: int
    user_id: int
    linkedin_url: str
